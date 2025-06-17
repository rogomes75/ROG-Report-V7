#!/usr/bin/env python3
import requests
import json
import base64
import os
import pandas as pd
import io
import time
import uuid
from datetime import datetime

# Get the backend URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"\'')
            break

# Ensure the backend URL is set
if not BACKEND_URL:
    raise ValueError("BACKEND_URL not found in frontend/.env")

# Add the /api prefix
API_URL = f"{BACKEND_URL}/api"
print(f"Using API URL: {API_URL}")

# Test results
test_results = {
    "Authentication system with JWT": {"success": False, "details": []},
    "User management system": {"success": False, "details": []},
    "Client management with Excel import": {"success": False, "details": []},
    "Service reports with photo upload": {"success": False, "details": []},
    "MongoDB database integration": {"success": False, "details": []}
}

# Helper function to log test results
def log_test(task, message, success=True):
    print(f"[{task}] {'✅ SUCCESS' if success else '❌ FAILURE'}: {message}")
    test_results[task]["details"].append({"success": success, "message": message})
    if not success:
        test_results[task]["success"] = False

# Helper function to set task success
def set_task_success(task):
    if all(detail["success"] for detail in test_results[task]["details"]):
        test_results[task]["success"] = True
    else:
        test_results[task]["success"] = False

# Test 1: Authentication System with JWT
print("\n=== Testing Authentication System with JWT ===\n")

# Test login with admin credentials
try:
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{API_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        login_result = response.json()
        admin_token = login_result["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        log_test("Authentication system with JWT", "Admin login successful")
        
        # Verify token contains expected data
        if "user" in login_result and login_result["user"]["role"] == "admin":
            log_test("Authentication system with JWT", "Token contains correct user data")
        else:
            log_test("Authentication system with JWT", "Token missing user data", False)
    else:
        log_test("Authentication system with JWT", f"Admin login failed: {response.text}", False)
        admin_token = None
        admin_headers = None
except Exception as e:
    log_test("Authentication system with JWT", f"Admin login exception: {str(e)}", False)
    admin_token = None
    admin_headers = None

# Test protected endpoint access
if admin_headers:
    try:
        response = requests.get(f"{API_URL}/auth/me", headers=admin_headers)
        if response.status_code == 200:
            user_data = response.json()
            if user_data["username"] == "admin" and user_data["role"] == "admin":
                log_test("Authentication system with JWT", "Protected endpoint access successful")
            else:
                log_test("Authentication system with JWT", "Protected endpoint returned incorrect data", False)
        else:
            log_test("Authentication system with JWT", f"Protected endpoint access failed: {response.text}", False)
    except Exception as e:
        log_test("Authentication system with JWT", f"Protected endpoint exception: {str(e)}", False)

# Test invalid login
try:
    login_data = {
        "username": "admin",
        "password": "wrongpassword"
    }
    response = requests.post(f"{API_URL}/auth/login", json=login_data)
    
    if response.status_code == 401:
        log_test("Authentication system with JWT", "Invalid login correctly rejected")
    else:
        log_test("Authentication system with JWT", f"Invalid login not properly handled: {response.text}", False)
except Exception as e:
    log_test("Authentication system with JWT", f"Invalid login exception: {str(e)}", False)

# Set overall success for Authentication
set_task_success("Authentication system with JWT")

# Test 2: User Management System
print("\n=== Testing User Management System ===\n")

if admin_headers:
    # Create a test user
    test_username = f"testuser_{uuid.uuid4().hex[:8]}"
    test_email = f"{test_username}@example.com"
    test_password = "testpassword123"
    
    try:
        user_data = {
            "username": test_username,
            "email": test_email,
            "password": test_password,
            "role": "employee"
        }
        response = requests.post(f"{API_URL}/users", json=user_data, headers=admin_headers)
        
        if response.status_code == 200:
            created_user = response.json()
            test_user_id = created_user["id"]
            log_test("User management system", f"User creation successful: {test_username}")
            
            # Verify user data
            if created_user["username"] == test_username and created_user["email"] == test_email:
                log_test("User management system", "Created user has correct data")
            else:
                log_test("User management system", "Created user has incorrect data", False)
                
            # Test user login
            try:
                login_data = {
                    "username": test_username,
                    "password": test_password
                }
                response = requests.post(f"{API_URL}/auth/login", json=login_data)
                
                if response.status_code == 200:
                    login_result = response.json()
                    user_token = login_result["access_token"]
                    user_headers = {"Authorization": f"Bearer {user_token}"}
                    log_test("User management system", f"New user login successful")
                    
                    # Test employee role restrictions
                    try:
                        response = requests.get(f"{API_URL}/users", headers=user_headers)
                        if response.status_code == 403:
                            log_test("User management system", "Employee role restrictions working correctly")
                        else:
                            log_test("User management system", "Employee role restrictions not enforced", False)
                    except Exception as e:
                        log_test("User management system", f"Role restriction test exception: {str(e)}", False)
                else:
                    log_test("User management system", f"New user login failed: {response.text}", False)
                    user_token = None
                    user_headers = None
            except Exception as e:
                log_test("User management system", f"New user login exception: {str(e)}", False)
                user_token = None
                user_headers = None
        else:
            log_test("User management system", f"User creation failed: {response.text}", False)
            test_user_id = None
    except Exception as e:
        log_test("User management system", f"User creation exception: {str(e)}", False)
        test_user_id = None
    
    # Test user listing
    try:
        response = requests.get(f"{API_URL}/users", headers=admin_headers)
        
        if response.status_code == 200:
            users = response.json()
            if isinstance(users, list) and len(users) > 0:
                log_test("User management system", f"User listing successful, found {len(users)} users")
                
                # Check if our test user is in the list
                if test_user_id and any(user["id"] == test_user_id for user in users):
                    log_test("User management system", "Test user found in user list")
                elif test_user_id:
                    log_test("User management system", "Test user not found in user list", False)
            else:
                log_test("User management system", "User listing returned empty or invalid data", False)
        else:
            log_test("User management system", f"User listing failed: {response.text}", False)
    except Exception as e:
        log_test("User management system", f"User listing exception: {str(e)}", False)
    
    # Test user deletion
    if test_user_id:
        try:
            response = requests.delete(f"{API_URL}/users/{test_user_id}", headers=admin_headers)
            
            if response.status_code == 200:
                log_test("User management system", f"User deletion successful: {test_username}")
                
                # Verify user is deleted
                response = requests.get(f"{API_URL}/users", headers=admin_headers)
                if response.status_code == 200:
                    users = response.json()
                    if not any(user["id"] == test_user_id for user in users):
                        log_test("User management system", "User deletion verified")
                    else:
                        log_test("User management system", "User still exists after deletion", False)
            else:
                log_test("User management system", f"User deletion failed: {response.text}", False)
        except Exception as e:
            log_test("User management system", f"User deletion exception: {str(e)}", False)
else:
    log_test("User management system", "Skipping user management tests due to failed admin login", False)

# Set overall success for User Management
set_task_success("User management system")

# Test 3: Client Management with Excel Import
print("\n=== Testing Client Management with Excel Import ===\n")

if admin_headers:
    # Create a test Excel file with client data
    try:
        # Create sample client data
        client_data = {
            "Name": ["Client 1", "Client 2", "Client 3"],
            "Address": ["123 Main St", "456 Oak Ave", "789 Pine Rd"]
        }
        df = pd.DataFrame(client_data)
        
        # Save to Excel file
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        
        # Upload Excel file
        files = {"file": ("clients.xlsx", excel_buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = requests.post(f"{API_URL}/clients/import-excel", files=files, headers={"Authorization": admin_headers["Authorization"]})
        
        if response.status_code == 200:
            import_result = response.json()
            log_test("Client management with Excel import", f"Excel import successful: {import_result['message']}")
        else:
            log_test("Client management with Excel import", f"Excel import failed: {response.text}", False)
    except Exception as e:
        log_test("Client management with Excel import", f"Excel import exception: {str(e)}", False)
    
    # Test client listing
    try:
        response = requests.get(f"{API_URL}/clients", headers=admin_headers)
        
        if response.status_code == 200:
            clients = response.json()
            if isinstance(clients, list):
                log_test("Client management with Excel import", f"Client listing successful, found {len(clients)} clients")
                
                # Check if our imported clients are in the list
                imported_clients = [c for c in clients if c["name"] in ["Client 1", "Client 2", "Client 3"]]
                if len(imported_clients) > 0:
                    log_test("Client management with Excel import", f"Found {len(imported_clients)} imported clients")
                else:
                    log_test("Client management with Excel import", "Imported clients not found in client list", False)
            else:
                log_test("Client management with Excel import", "Client listing returned invalid data", False)
        else:
            log_test("Client management with Excel import", f"Client listing failed: {response.text}", False)
    except Exception as e:
        log_test("Client management with Excel import", f"Client listing exception: {str(e)}", False)
    
    # Test client creation directly
    try:
        client_data = {
            "name": f"Test Client {uuid.uuid4().hex[:8]}",
            "address": "Test Address"
        }
        response = requests.post(f"{API_URL}/clients", json=client_data, headers=admin_headers)
        
        if response.status_code == 200:
            created_client = response.json()
            log_test("Client management with Excel import", f"Client creation successful: {created_client['name']}")
        else:
            log_test("Client management with Excel import", f"Client creation failed: {response.text}", False)
    except Exception as e:
        log_test("Client management with Excel import", f"Client creation exception: {str(e)}", False)
else:
    log_test("Client management with Excel import", "Skipping client management tests due to failed admin login", False)

# Set overall success for Client Management
set_task_success("Client management with Excel import")

# Test 4: Service Reports with Photo Upload
print("\n=== Testing Service Reports with Photo Upload ===\n")

if admin_headers:
    # Get a client ID for testing
    client_id = None
    try:
        response = requests.get(f"{API_URL}/clients", headers=admin_headers)
        if response.status_code == 200:
            clients = response.json()
            if clients:
                client_id = clients[0]["id"]
                log_test("Service reports with photo upload", f"Found client for testing: {clients[0]['name']}")
            else:
                log_test("Service reports with photo upload", "No clients found for testing", False)
        else:
            log_test("Service reports with photo upload", f"Failed to get clients for testing: {response.text}", False)
    except Exception as e:
        log_test("Service reports with photo upload", f"Client retrieval exception: {str(e)}", False)
    
    # Create a test service report with photos
    if client_id:
        try:
            # Create a sample base64 image
            sample_image = base64.b64encode(b"This is a test image").decode('utf-8')
            
            report_data = {
                "client_id": client_id,
                "description": "Test service report with photos",
                "photos": [sample_image, sample_image],  # Add two sample images
                "priority": "URGENT"
            }
            
            response = requests.post(f"{API_URL}/reports", json=report_data, headers=admin_headers)
            
            if response.status_code == 200:
                created_report = response.json()
                report_id = created_report["id"]
                log_test("Service reports with photo upload", f"Service report creation successful")
                
                # Verify report data
                if (created_report["client_id"] == client_id and 
                    created_report["description"] == "Test service report with photos" and
                    len(created_report["photos"]) == 2):
                    log_test("Service reports with photo upload", "Created report has correct data")
                else:
                    log_test("Service reports with photo upload", "Created report has incorrect data", False)
                
                # Test report listing
                try:
                    response = requests.get(f"{API_URL}/reports", headers=admin_headers)
                    
                    if response.status_code == 200:
                        reports = response.json()
                        if isinstance(reports, list) and len(reports) > 0:
                            log_test("Service reports with photo upload", f"Report listing successful, found {len(reports)} reports")
                            
                            # Check if our test report is in the list
                            if any(report["id"] == report_id for report in reports):
                                log_test("Service reports with photo upload", "Test report found in report list")
                            else:
                                log_test("Service reports with photo upload", "Test report not found in report list", False)
                        else:
                            log_test("Service reports with photo upload", "Report listing returned empty or invalid data", False)
                    else:
                        log_test("Service reports with photo upload", f"Report listing failed: {response.text}", False)
                except Exception as e:
                    log_test("Service reports with photo upload", f"Report listing exception: {str(e)}", False)
                
                # Test report status update
                try:
                    update_data = {
                        "status": "scheduled",
                        "admin_notes": "Test admin notes"
                    }
                    
                    response = requests.put(f"{API_URL}/reports/{report_id}", json=update_data, headers=admin_headers)
                    
                    if response.status_code == 200:
                        updated_report = response.json()
                        log_test("Service reports with photo upload", f"Report status update successful")
                        
                        # Verify update
                        if (updated_report["status"] == "scheduled" and 
                            updated_report["admin_notes"] == "Test admin notes"):
                            log_test("Service reports with photo upload", "Report update verified")
                        else:
                            log_test("Service reports with photo upload", "Report update not applied correctly", False)
                    else:
                        log_test("Service reports with photo upload", f"Report status update failed: {response.text}", False)
                except Exception as e:
                    log_test("Service reports with photo upload", f"Report status update exception: {str(e)}", False)
            else:
                log_test("Service reports with photo upload", f"Service report creation failed: {response.text}", False)
                report_id = None
        except Exception as e:
            log_test("Service reports with photo upload", f"Service report creation exception: {str(e)}", False)
            report_id = None
    else:
        log_test("Service reports with photo upload", "Skipping service report tests due to no available clients", False)
else:
    log_test("Service reports with photo upload", "Skipping service report tests due to failed admin login", False)

# Set overall success for Service Reports
set_task_success("Service reports with photo upload")

# Test 5: MongoDB Database Integration
print("\n=== Testing MongoDB Database Integration ===\n")

# This is implicitly tested through the other tests, but we'll add some specific checks
if admin_headers:
    # Check if data persists after multiple requests
    try:
        # Get users count
        response = requests.get(f"{API_URL}/users", headers=admin_headers)
        if response.status_code == 200:
            users_count_1 = len(response.json())
            
            # Create a new user
            test_username = f"dbtest_{uuid.uuid4().hex[:8]}"
            user_data = {
                "username": test_username,
                "email": f"{test_username}@example.com",
                "password": "testpassword123",
                "role": "employee"
            }
            response = requests.post(f"{API_URL}/users", json=user_data, headers=admin_headers)
            
            if response.status_code == 200:
                created_user = response.json()
                test_user_id = created_user["id"]
                
                # Get users count again
                response = requests.get(f"{API_URL}/users", headers=admin_headers)
                if response.status_code == 200:
                    users_count_2 = len(response.json())
                    
                    if users_count_2 == users_count_1 + 1:
                        log_test("MongoDB database integration", "Data persistence verified: user count increased after creation")
                    else:
                        log_test("MongoDB database integration", f"Data persistence issue: user count before={users_count_1}, after={users_count_2}", False)
                    
                    # Clean up test user
                    requests.delete(f"{API_URL}/users/{test_user_id}", headers=admin_headers)
                else:
                    log_test("MongoDB database integration", f"Failed to get users after creation: {response.text}", False)
            else:
                log_test("MongoDB database integration", f"Failed to create test user for DB test: {response.text}", False)
        else:
            log_test("MongoDB database integration", f"Failed to get initial users count: {response.text}", False)
    except Exception as e:
        log_test("MongoDB database integration", f"Database persistence test exception: {str(e)}", False)
    
    # Check if we can retrieve data by ID
    try:
        # Get clients
        response = requests.get(f"{API_URL}/clients", headers=admin_headers)
        if response.status_code == 200:
            clients = response.json()
            if clients:
                # Create a service report for a client
                client_id = clients[0]["id"]
                report_data = {
                    "client_id": client_id,
                    "description": "Database test report",
                    "photos": [],
                    "priority": "NEXT WEEK"
                }
                
                response = requests.post(f"{API_URL}/reports", json=report_data, headers=admin_headers)
                if response.status_code == 200:
                    report = response.json()
                    report_id = report["id"]
                    
                    # Update the report
                    update_data = {
                        "status": "in_progress",
                        "admin_notes": "Testing database updates"
                    }
                    
                    response = requests.put(f"{API_URL}/reports/{report_id}", json=update_data, headers=admin_headers)
                    if response.status_code == 200:
                        # Get all reports
                        response = requests.get(f"{API_URL}/reports", headers=admin_headers)
                        if response.status_code == 200:
                            reports = response.json()
                            updated_report = next((r for r in reports if r["id"] == report_id), None)
                            
                            if updated_report and updated_report["status"] == "in_progress":
                                log_test("MongoDB database integration", "Database update and retrieval verified")
                            else:
                                log_test("MongoDB database integration", "Database update not reflected in retrieved data", False)
                        else:
                            log_test("MongoDB database integration", f"Failed to get reports after update: {response.text}", False)
                    else:
                        log_test("MongoDB database integration", f"Failed to update report: {response.text}", False)
                else:
                    log_test("MongoDB database integration", f"Failed to create report for DB test: {response.text}", False)
            else:
                log_test("MongoDB database integration", "No clients found for database test", False)
        else:
            log_test("MongoDB database integration", f"Failed to get clients for database test: {response.text}", False)
    except Exception as e:
        log_test("MongoDB database integration", f"Database retrieval test exception: {str(e)}", False)
else:
    log_test("MongoDB database integration", "Skipping database integration tests due to failed admin login", False)

# Set overall success for MongoDB Integration
set_task_success("MongoDB database integration")

# Print summary
print("\n=== Test Summary ===\n")
for task, result in test_results.items():
    status = "✅ PASSED" if result["success"] else "❌ FAILED"
    print(f"{task}: {status}")
    for detail in result["details"]:
        status_icon = "✅" if detail["success"] else "❌"
        print(f"  {status_icon} {detail['message']}")
    print()

# Return overall success status
all_passed = all(result["success"] for result in test_results.values())
print(f"\nOverall Test Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")