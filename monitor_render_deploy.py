#!/usr/bin/env python3
"""
Monitor Render Deploy Status
"""

import requests
import time
import json

def check_render_version():
    url = "https://rog-report-v5.onrender.com/"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            version = data.get('version', 'unknown')
            message = data.get('message', '')
            
            return {
                'status': 'success',
                'version': version,
                'message': message,
                'is_v3': version == '3.0',
                'has_pool_message': 'Pool Service' in message
            }
        else:
            return {'status': 'error', 'code': response.status_code}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def monitor_deploy(max_attempts=10, interval=30):
    print("🔄 Monitoring Render Deploy Status")
    print("=" * 50)
    
    for attempt in range(1, max_attempts + 1):
        print(f"⏰ Attempt {attempt}/{max_attempts} - {time.strftime('%H:%M:%S')}")
        
        result = check_render_version()
        
        if result['status'] == 'success':
            print(f"  ✅ Response received")
            print(f"  📌 Version: {result['version']}")
            print(f"  📝 Message: {result['message'][:60]}...")
            
            if result['is_v3'] and result['has_pool_message']:
                print("\n🎉 SUCCESS! v3.0 deployed successfully!")
                print("✅ ROG Pool Service v3.0 is live!")
                return True
            elif result['version'] != 'unknown':
                print(f"  ⚠️  Still showing v{result['version']} - waiting...")
            else:
                print("  ⏳ Old version detected - waiting for update...")
                
        else:
            print(f"  ❌ Error: {result.get('error', result.get('code', 'Unknown'))}")
        
        if attempt < max_attempts:
            print(f"  💤 Waiting {interval}s for next check...")
            time.sleep(interval)
        print()
    
    print("❌ Deploy monitoring timeout - check Render dashboard manually")
    return False

if __name__ == "__main__":
    print("🚀 Starting Render Deploy Monitor")
    print("This will check every 30s for v3.0 deployment")
    print("Press Ctrl+C to stop\n")
    
    try:
        success = monitor_deploy()
        if success:
            print("\n🌐 Test the new features:")
            print("   - Interface: https://rog-report-v5.onrender.com/html")
            print("   - API: https://rog-report-v5.onrender.com/api/")
            print("   - Clients: https://rog-report-v5.onrender.com/api/clients")
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")