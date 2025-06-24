#!/usr/bin/env python3
"""
ROG Pool Service - Quick Deploy Script
One-click preparation for Railway deployment
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def quick_deploy():
    print("🚀 ROG Pool Service - Quick Deploy Setup")
    print("=" * 50)
    
    # 1. Check if we're in the right place
    if not (Path("frontend").exists() and Path("backend").exists()):
        print("❌ Error: Not in project root directory")
        sys.exit(1)
    
    print("✅ Project structure validated")
    
    # 2. Install frontend deps and build
    print("📦 Installing frontend dependencies...")
    success, _ = run_cmd("npm install", cwd="frontend")
    if not success:
        print("❌ Frontend dependency installation failed")
        sys.exit(1)
    
    print("🏗️  Building frontend...")
    success, _ = run_cmd("npm run build", cwd="frontend")
    if not success:
        print("❌ Frontend build failed")
        sys.exit(1)
    
    print("✅ Frontend built successfully")
    
    # 3. Git operations
    print("📝 Preparing Git commit...")
    
    # Add all files
    run_cmd("git add .")
    
    # Commit if there are changes
    success, _ = run_cmd("git diff --staged --quiet")
    if not success:  # There are staged changes
        commit_msg = f"Deploy preparation - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        success, _ = run_cmd(f'git commit -m "{commit_msg}"')
        if success:
            print("✅ Changes committed")
        else:
            print("⚠️  Commit failed (maybe no changes)")
    else:
        print("ℹ️  No changes to commit")
    
    # 4. Environment template
    env_content = """# Railway Environment Variables Template
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/pool_maintenance_db
DB_NAME=pool_maintenance_db
REACT_APP_BACKEND_URL=https://your-app-name.railway.app
SECRET_KEY=pool_maintenance_secret_key_2024
NODE_ENV=production
PYTHON_ENV=production
"""
    
    with open(".env.railway", "w") as f:
        f.write(env_content)
    
    print("✅ Environment template created (.env.railway)")
    
    # 5. Final checklist
    checklist = {
        "nixpacks.toml": Path("nixpacks.toml").exists(),
        "railway.json": Path("railway.json").exists(),
        "Procfile": Path("Procfile").exists(),
        "Frontend build": Path("frontend/build").exists(),
        "Backend requirements": Path("backend/requirements.txt").exists(),
        "Environment template": Path(".env.railway").exists()
    }
    
    print("\n📋 Deployment Readiness Checklist:")
    all_good = True
    for item, status in checklist.items():
        if status:
            print(f"  ✅ {item}")
        else:
            print(f"  ❌ {item}")
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 READY FOR RAILWAY DEPLOYMENT!")
        print("\nNext steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Go to https://railway.app")
        print("3. Connect your GitHub repo")
        print("4. Set environment variables from .env.railway")
        print("5. Deploy and test with admin/admin123")
    else:
        print("⚠️  Some files are missing. Please run the full setup script.")
    
    print("=" * 50)

if __name__ == "__main__":
    quick_deploy()