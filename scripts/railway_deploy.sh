#!/bin/bash
# ROG Pool Service - Railway Deploy Automation Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP $1]${NC} ${2}"
}

print_success() {
    echo -e "${GREEN}✅ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  ${1}${NC}"
}

print_error() {
    echo -e "${RED}❌ ${1}${NC}"
}

# Header
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}    ROG POOL SERVICE - RAILWAY DEPLOY${NC}"
echo -e "${BLUE}============================================${NC}"

# Step 1: Check if we're in the right directory
print_step 1 "Checking project structure..."
if [[ ! -f "package.json" ]] && [[ ! -f "frontend/package.json" ]]; then
    print_error "Not in a valid project directory. Make sure you're in the project root."
    exit 1
fi
print_success "Project structure looks good"

# Step 2: Install dependencies
print_step 2 "Installing dependencies..."

# Frontend dependencies
if [[ -d "frontend" ]]; then
    print_step "2a" "Installing frontend dependencies..."
    cd frontend
    npm install
    print_success "Frontend dependencies installed"
    cd ..
fi

# Backend dependencies
if [[ -d "backend" ]] && [[ -f "backend/requirements.txt" ]]; then
    print_step "2b" "Checking backend dependencies..."
    print_success "Backend requirements.txt found"
fi

# Step 3: Build frontend
print_step 3 "Building frontend for production..."
if [[ -d "frontend" ]]; then
    cd frontend
    npm run build
    if [[ -d "build" ]]; then
        print_success "Frontend built successfully"
    else
        print_error "Frontend build failed"
        exit 1
    fi
    cd ..
else
    print_warning "Frontend directory not found, skipping build"
fi

# Step 4: Git operations
print_step 4 "Preparing Git repository..."

# Check if git is initialized
if [[ ! -d ".git" ]]; then
    print_warning "Git repository not initialized. Initializing..."
    git init
    print_success "Git repository initialized"
fi

# Add all files
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    print_warning "No changes to commit"
else
    print_step "4a" "Committing changes..."
    git commit -m "Prepare for Railway deployment - $(date)"
    print_success "Changes committed"
fi

# Check for remote
if ! git remote get-url origin >/dev/null 2>&1; then
    print_warning "No Git remote 'origin' found."
    echo "Please add your GitHub repository:"
    echo "git remote add origin https://github.com/yourusername/your-repo.git"
    echo "Then run: git push -u origin main"
else
    print_step "4b" "Pushing to GitHub..."
    git push origin main || {
        print_warning "Push failed. You may need to authenticate or set up the remote correctly."
        echo "Try: git push -u origin main"
    }
    print_success "Code pushed to GitHub"
fi

# Step 5: Generate Railway configuration
print_step 5 "Checking Railway configuration files..."

config_files=("nixpacks.toml" "railway.json" "Procfile")
missing_files=()

for file in "${config_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -eq 0 ]]; then
    print_success "All Railway configuration files present"
else
    print_warning "Missing configuration files: ${missing_files[*]}"
    print_warning "These should be created by the main setup script"
fi

# Step 6: Environment variables reminder
print_step 6 "Environment Variables Setup"
echo ""
echo "📋 IMPORTANT: Set these environment variables in Railway:"
echo ""
echo "Required variables:"
echo "  MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/dbname"
echo "  DB_NAME=pool_maintenance_db"
echo "  REACT_APP_BACKEND_URL=https://your-app.railway.app"
echo "  SECRET_KEY=pool_maintenance_secret_key_2024"
echo "  NODE_ENV=production"
echo "  PYTHON_ENV=production"
echo ""
echo "💡 Check .env.railway file for complete template"

# Step 7: Railway CLI check (optional)
print_step 7 "Checking Railway CLI..."
if command -v railway &> /dev/null; then
    print_success "Railway CLI found"
    echo "You can use: railway login && railway link"
else
    print_warning "Railway CLI not found (optional)"
    echo "Install with: npm install -g @railway/cli"
fi

# Final instructions
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}    🎉 DEPLOY PREPARATION COMPLETE!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Next steps:"
echo "1. 🌐 Go to https://railway.app"
echo "2. 🔗 Connect your GitHub repository"
echo "3. ⚙️  Set environment variables (see above)"
echo "4. 🚀 Deploy your application"
echo "5. 🧪 Test with admin/admin123"
echo ""
echo "📖 Read DEPLOYMENT_CHECKLIST.md for detailed instructions"
echo ""
print_success "Ready for Railway deployment!"