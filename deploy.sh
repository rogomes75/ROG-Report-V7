#!/bin/bash
# ROG Pool Service - One-Click Deploy Script
# Este script executa TUDO automaticamente

echo "🚀 ROG POOL SERVICE - ONE-CLICK DEPLOY"
echo "======================================"

# Execute the main setup
echo "1️⃣ Running complete setup..."
python scripts/deploy_setup.py

echo ""
echo "2️⃣ Running quick build and commit..."
python scripts/quick_deploy.py

echo ""
echo "======================================"
echo "🎉 DEPLOY PREPARATION COMPLETE!"
echo "======================================"
echo ""
echo "📋 NEXT STEPS:"
echo "1. 🌐 Go to https://railway.app"
echo "2. 📂 Connect your GitHub repository"
echo "3. ⚙️  Set environment variables from .env.railway file"
echo "4. 🚀 Click Deploy"
echo "5. 🧪 Test with: python scripts/test_deployment.py YOUR_RAILWAY_URL"
echo ""
echo "📖 Check DEPLOYMENT_CHECKLIST.md for detailed steps"
echo "🔑 Login credentials: admin/admin123"
echo ""
echo "✨ Your ROG Pool Service is ready for Railway!"