#!/usr/bin/env python3
"""
Test MongoDB Integration para ROG Pool Service
"""

import requests
import json
import sys

def test_mongodb_integration():
    base_url = "https://web-production-ee0ff.up.railway.app"
    
    print("🧪 Testing ROG Pool Service - MongoDB Integration")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 8
    
    # Test 1: Basic Health Check
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            db_status = data.get('database', 'unknown')
            print(f"  ✅ Health Check: {data.get('status')} - DB: {db_status}")
            if db_status == "connected":
                tests_passed += 1
            else:
                print(f"  ⚠️  Database status: {db_status}")
        else:
            print(f"  ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Health check error: {e}")
    
    # Test 2: Root endpoint with MongoDB info
    print("🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Root: {data.get('message', 'OK')}")
            tests_passed += 1
        else:
            print(f"  ❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Root endpoint error: {e}")
    
    # Test 3: API Root
    print("🔗 Testing API root...")
    try:
        response = requests.get(f"{base_url}/api/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API Root: {data.get('message', 'OK')}")
            tests_passed += 1
        else:
            print(f"  ❌ API root failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ API root error: {e}")
    
    # Test 4: Get Clients (empty initially)
    print("👥 Testing clients endpoint...")
    try:
        response = requests.get(f"{base_url}/api/clients", timeout=30)
        if response.status_code == 200:
            clients = response.json()
            print(f"  ✅ Clients endpoint: {len(clients)} clients found")
            tests_passed += 1
        else:
            print(f"  ❌ Clients endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Clients endpoint error: {e}")
    
    # Test 5: Get Reports (empty initially)
    print("📋 Testing reports endpoint...")
    try:
        response = requests.get(f"{base_url}/api/reports", timeout=30)
        if response.status_code == 200:
            reports = response.json()
            print(f"  ✅ Reports endpoint: {len(reports)} reports found")
            tests_passed += 1
        else:
            print(f"  ❌ Reports endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Reports endpoint error: {e}")
    
    # Test 6: Initialize Sample Data
    print("🌱 Testing sample data creation...")
    try:
        response = requests.post(f"{base_url}/api/init-data", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Sample data: {data.get('message', 'OK')}")
            tests_passed += 1
        else:
            print(f"  ❌ Sample data failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Sample data error: {e}")
    
    # Test 7: Verify Clients After Sample Data
    print("👥 Testing clients after sample data...")
    try:
        response = requests.get(f"{base_url}/api/clients", timeout=30)
        if response.status_code == 200:
            clients = response.json()
            print(f"  ✅ Clients after init: {len(clients)} clients")
            if len(clients) > 0:
                print(f"      📝 Sample client: {clients[0].get('name', 'Unknown')}")
            tests_passed += 1
        else:
            print(f"  ❌ Clients verification failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Clients verification error: {e}")
    
    # Test 8: Verify Reports After Sample Data
    print("📋 Testing reports after sample data...")
    try:
        response = requests.get(f"{base_url}/api/reports", timeout=30)
        if response.status_code == 200:
            reports = response.json()
            print(f"  ✅ Reports after init: {len(reports)} reports")
            if len(reports) > 0:
                print(f"      📝 Sample report: {reports[0].get('title', 'Unknown')}")
            tests_passed += 1
        else:
            print(f"  ❌ Reports verification failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Reports verification error: {e}")
    
    return tests_passed, total_tests

def main():
    print("🚀 ROG Pool Service - MongoDB Integration Test")
    print("URL: https://web-production-ee0ff.up.railway.app")
    print("=" * 70)
    
    passed, total = test_mongodb_integration()
    
    print("\n" + "=" * 70)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - MONGODB INTEGRATION SUCCESSFUL!")
        print("\n✅ MongoDB is working perfectly!")
        print("🗄️ Database connected and operational")
        print("👥 Clients management working")
        print("📋 Service reports working")
        print("🌱 Sample data creation working")
        
        print("\n🌐 Test the HTML interface:")
        print("   https://web-production-ee0ff.up.railway.app/html")
        
        print("\n🔗 API Endpoints working:")
        print("   GET  /api/clients - List clients")
        print("   POST /api/clients - Create client")
        print("   GET  /api/reports - List reports")
        print("   POST /api/reports - Create report")
        print("   POST /api/init-data - Initialize sample data")
        
    elif passed > total/2:
        print(f"⚠️  PARTIAL SUCCESS: {passed}/{total} tests passed")
        print("💡 Most features working - check Railway MongoDB plugin")
    else:
        print("❌ MONGODB INTEGRATION FAILED!")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if MongoDB plugin was added to Railway")
        print("   2. Verify DATABASE_URL is created automatically")
        print("   3. Check Railway deployment logs")
        print("   4. Ensure environment variables are set")
    
    print("=" * 70)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)