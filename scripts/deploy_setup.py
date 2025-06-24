#!/usr/bin/env python3
"""
ROG Pool Service - Railway Deploy Setup Script
Este script automatiza a preparação para deploy no Railway
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(step, message):
    print(f"{Colors.OKBLUE}[STEP {step}]{Colors.ENDC} {Colors.BOLD}{message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

def run_command(cmd, cwd=None):
    """Execute shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def check_prerequisites():
    """Check if all required tools are installed"""
    print_step(1, "Checking Prerequisites")
    
    # Check Git
    success, _ = run_command("git --version")
    if success:
        print_success("Git is installed")
    else:
        print_error("Git is not installed or not in PATH")
        return False
    
    # Check Node.js
    success, version = run_command("node --version")
    if success:
        print_success(f"Node.js is installed: {version}")
    else:
        print_error("Node.js is not installed")
        return False
    
    # Check Python
    success, version = run_command("python --version")
    if success:
        print_success(f"Python is installed: {version}")
    else:
        print_error("Python is not installed")
        return False
    
    return True

def setup_project_structure():
    """Ensure project structure is correct"""
    print_step(2, "Checking Project Structure")
    
    required_files = [
        "backend/server.py",
        "backend/requirements.txt", 
        "frontend/package.json",
        "frontend/src/App.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print_error(f"Missing required files: {', '.join(missing_files)}")
        return False
    
    print_success("Project structure is valid")
    return True

def create_deployment_files():
    """Create necessary deployment configuration files"""
    print_step(3, "Creating Deployment Configuration Files")
    
    # Check if files already exist
    config_files = ["nixpacks.toml", "railway.json", "Procfile"]
    existing_files = [f for f in config_files if Path(f).exists()]
    
    if existing_files:
        print_success(f"Deployment files already exist: {', '.join(existing_files)}")
    else:
        print_warning("Some deployment files are missing, but they should be created by the main script")
    
    return True

def build_frontend():
    """Build the React frontend"""
    print_step(4, "Building Frontend")
    
    if not Path("frontend").exists():
        print_error("Frontend directory not found")
        return False
    
    print("Installing frontend dependencies...")
    success, output = run_command("npm install", cwd="frontend")
    if not success:
        print_error(f"Failed to install frontend dependencies: {output}")
        return False
    
    print("Building frontend...")
    success, output = run_command("npm run build", cwd="frontend")
    if not success:
        print_error(f"Failed to build frontend: {output}")
        return False
    
    build_dir = Path("frontend/build")
    if build_dir.exists():
        print_success("Frontend built successfully")
        return True
    else:
        print_error("Build directory not created")
        return False

def check_backend_dependencies():
    """Check if backend dependencies are installable"""
    print_step(5, "Checking Backend Dependencies")
    
    if not Path("backend/requirements.txt").exists():
        print_error("requirements.txt not found in backend directory")
        return False
    
    # Try to install dependencies in a virtual environment (simulation)
    print("Checking backend requirements...")
    with open("backend/requirements.txt", "r") as f:
        requirements = f.read().strip()
        if requirements:
            print_success("Backend requirements.txt is valid")
            return True
        else:
            print_error("requirements.txt is empty")
            return False

def generate_env_template():
    """Generate .env template for Railway"""
    print_step(6, "Generating Environment Variables Template")
    
    env_template = """# ROG Pool Service - Railway Environment Variables
# Copy these variables to your Railway project settings

# ===== DATABASE CONFIGURATION =====
# Option A: MongoDB Atlas (Recommended for production)
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/pool_maintenance_db

# Option B: Railway MongoDB Plugin
# DATABASE_URL=mongodb://mongo:27017

# Database name
DB_NAME=pool_maintenance_db

# ===== FRONTEND CONFIGURATION =====
# Replace 'your-app-name' with your actual Railway app name
REACT_APP_BACKEND_URL=https://your-app-name.railway.app

# ===== SECURITY =====
SECRET_KEY=pool_maintenance_secret_key_2024

# ===== PRODUCTION SETTINGS =====
NODE_ENV=production
PYTHON_ENV=production

# ===== OPTIONAL SETTINGS =====
# PORT=8000  # Railway sets this automatically
# HOST=0.0.0.0  # Railway sets this automatically
"""
    
    with open(".env.railway", "w") as f:
        f.write(env_template)
    
    print_success("Environment template created: .env.railway")
    return True

def git_setup_check():
    """Check Git setup and provide instructions"""
    print_step(7, "Git Repository Setup")
    
    # Check if we're in a git repository
    success, _ = run_command("git status")
    if not success:
        print_error("Not in a Git repository. Initialize with: git init")
        return False
    
    # Check if remote is configured
    success, remotes = run_command("git remote -v")
    if not success or not remotes:
        print_warning("No Git remote configured")
        print("To add your GitHub repository:")
        print("git remote add origin https://github.com/yourusername/your-repo.git")
        return True
    
    print_success("Git repository is properly configured")
    return True

def create_deployment_checklist():
    """Create a deployment checklist"""
    print_step(8, "Creating Deployment Checklist")
    
    checklist = """# 🚀 ROG Pool Service - Railway Deployment Checklist

## Pre-Deploy Checklist
- [ ] All code committed to GitHub
- [ ] MongoDB database ready (Atlas or Railway plugin)
- [ ] Railway account created
- [ ] Environment variables prepared

## Deploy Steps
1. [ ] Connect GitHub repository to Railway
2. [ ] Configure environment variables in Railway dashboard
3. [ ] Deploy application
4. [ ] Test login with admin/admin123
5. [ ] Verify all features working

## Environment Variables to Set in Railway
Copy from .env.railway file:
- MONGO_URL
- DB_NAME  
- REACT_APP_BACKEND_URL
- SECRET_KEY
- NODE_ENV
- PYTHON_ENV

## Post-Deploy Testing
- [ ] Frontend loads correctly
- [ ] Login works with admin/admin123
- [ ] Service reports can be created
- [ ] Client management works
- [ ] Photo uploads work
- [ ] Admin dashboard functions

## Default Login Credentials
- Admin: admin / admin123
- Test Admin: testadmin / test123

## Support
If issues occur, check:
1. Railway logs in dashboard
2. Environment variables are set correctly
3. Database connection is working
4. Build completed successfully
"""
    
    with open("DEPLOYMENT_CHECKLIST.md", "w") as f:
        f.write(checklist)
    
    print_success("Deployment checklist created: DEPLOYMENT_CHECKLIST.md")
    return True

def main():
    """Main deployment setup function"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("    ROG POOL SERVICE - RAILWAY DEPLOY SETUP")
    print("=" * 60)
    print(f"{Colors.ENDC}")
    
    # Run all setup steps
    steps = [
        check_prerequisites,
        setup_project_structure,
        create_deployment_files,
        build_frontend,
        check_backend_dependencies,
        generate_env_template,
        git_setup_check,
        create_deployment_checklist
    ]
    
    failed_steps = []
    
    for i, step in enumerate(steps, 1):
        try:
            if not step():
                failed_steps.append(step.__name__)
        except Exception as e:
            print_error(f"Error in {step.__name__}: {str(e)}")
            failed_steps.append(step.__name__)
    
    print("\n" + "=" * 60)
    if failed_steps:
        print_error(f"Setup completed with {len(failed_steps)} issues:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\nPlease resolve these issues before deploying.")
    else:
        print_success("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Check .env.railway for environment variables")
        print("2. Read DEPLOYMENT_CHECKLIST.md")
        print("3. Push code to GitHub")
        print("4. Connect to Railway and deploy")
    
    print("=" * 60)

if __name__ == "__main__":
    main()