#!/bin/bash
# ============================================================================
# ProjectMaker - Automated Setup Script
# Project: SocialBunny
# Generated: Making Social App By Hani
# ============================================================================

set -e  # Exit on any error

echo "🚀 Starting setup for SocialBunny..."

# Colors for output
GREEN='\033[0.32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================================================
# STEP 1: Git Repository Setup
# ============================================================================

echo "${BLUE}📦 Initializing Git...${{NC}}"
git init
echo "${GREEN}✅ Git initialized${{NC}}"

# ============================================================================
# STEP 2: Backend Setup (FASTAPI)
# ============================================================================
echo "${BLUE}🐍 Setting up Python backend...${NC}"
cd backend

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt


echo "${GREEN}✅ Backend setup complete!${NC}"
cd ..

# ============================================================================
# STEP 3: Frontend Setup (REACT)
# ============================================================================
echo "${BLUE}🎨 Setting up frontend...${NC}"
cd frontend

# Install dependencies (using legacy peer deps for compatibility)
echo "Installing npm packages..."
npm install

echo "${GREEN}✅ Frontend setup complete!${NC}"
cd ..

# ============================================================================
# STEP 4: Database Setup (MYSQL)
# ============================================================================
echo "${BLUE}🗄️  Setting up database...${NC}"
# Run the database setup script
bash db_setup.sh
echo "${GREEN}✅ Database setup complete!${NC}"

# ============================================================================
# SETUP COMPLETE! 🎉
# ============================================================================
echo ""
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}   ✨ Setup Complete for SocialBunny! ✨${NC}"
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "${BLUE}📝 Next Steps:${NC}"
echo ""
echo "1. Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Start Frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "🔗 Visit: http://localhost:3000 (frontend)"
echo "🔗 API: http://localhost:8000 (backend)"
echo ""
echo "${GREEN}Happy coding! 🚀${NC}"
