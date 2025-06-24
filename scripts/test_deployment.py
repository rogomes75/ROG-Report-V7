#!/usr/bin/env python3
"""
ROG Pool Service - Deployment Test Script
Test your Railway deployment for common issues
"""

import requests
import time
import sys
from urllib.parse import urljoin

class DeploymentTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.session.timeout = 30
        
    def test_health_check(self):
        """Test basic API health"""
        print("🏥 Testing API health...")
        try:
            response = self.session.get(f"{self.api_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ API is responding: {data.get('message', 'OK')}")
                return True
            else:
                print(f"  ❌ API health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ API health check error: {e}")
            return False
    
    def test_frontend(self):
        """Test if frontend is loading"""
        print("🌐 Testing frontend...")
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                if "ROG Pool Service" in response.text or "react" in response.text.lower():
                    print("  ✅ Frontend is loading")
                    return True
                else:
                    print("  ⚠️  Frontend loaded but content might be wrong")
                    return False
            else:
                print(f"  ❌ Frontend not accessible: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Frontend test error: {e}")
            return False
    
    def test_authentication(self):
        """Test login functionality"""
        print("🔐 Testing authentication...")
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            response = self.session.post(f"{self.api_url}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    print("  ✅ Authentication working")
                    self.token = data["access_token"]
                    return True
                else:
                    print("  ❌ Authentication response invalid")
                    return False
            else:
                print(f"  ❌ Authentication failed: {response.status_code}")
                if response.status_code == 401:
                    print("    💡 Check if admin user exists in database")
                return False
        except Exception as e:
            print(f"  ❌ Authentication test error: {e}")
            return False
    
    def test_database_connectivity(self):
        """Test database operations"""
        print("🗄️  Testing database connectivity...")
        if not hasattr(self, 'token'):
            print("  ⚠️  Skipping database test - no auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Test getting users (admin only endpoint)
            response = self.session.get(f"{self.api_url}/users", headers=headers)
            
            if response.status_code == 200:
                users = response.json()
                print(f"  ✅ Database connected - found {len(users)} users")
                return True
            else:
                print(f"  ❌ Database test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Database test error: {e}")
            return False
    
    def test_api_endpoints(self):
        """Test key API endpoints"""
        print("🔗 Testing API endpoints...")
        if not hasattr(self, 'token'):
            print("  ⚠️  Skipping API test - no auth token")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        endpoints = [
            ("/auth/me", "User profile"),
            ("/clients", "Clients list"),
            ("/reports", "Service reports")
        ]
        
        success_count = 0
        for endpoint, description in endpoints:
            try:
                response = self.session.get(f"{self.api_url}{endpoint}", headers=headers)
                if response.status_code == 200:
                    print(f"  ✅ {description} endpoint working")
                    success_count += 1
                else:
                    print(f"  ❌ {description} endpoint failed: {response.status_code}")
            except Exception as e:
                print(f"  ❌ {description} endpoint error: {e}")
        
        return success_count == len(endpoints)
    
    def run_full_test(self):
        """Run all tests"""
        print(f"🧪 Testing deployment at: {self.base_url}")
        print("=" * 60)
        
        tests = [
            self.test_frontend,
            self.test_health_check,
            self.test_authentication,
            self.test_database_connectivity,
            self.test_api_endpoints
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()  # Empty line between tests
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your deployment is working correctly.")
            print("\n💡 You can now login with:")
            print("   Username: admin")
            print("   Password: admin123")
        elif passed >= total - 1:
            print("⚠️  Almost there! Only minor issues detected.")
        else:
            print("❌ Several issues detected. Check the errors above.")
            print("\n🔧 Common solutions:")
            print("   - Check environment variables are set correctly")
            print("   - Verify MongoDB connection")
            print("   - Check Railway logs for errors")
        
        return passed == total

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <your-railway-app-url>")
        print("Example: python test_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    app_url = sys.argv[1]
    tester = DeploymentTester(app_url)
    success = tester.run_full_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()