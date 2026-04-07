#!/bin/bash

# Team Mistral - Oracle Forge Setup Script
# Run: chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🔮 Setting up Mistral Oracle Forge..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r agent/requirements.txt

# Copy environment template
echo "⚙️ Setting up environment variables..."
cp .env.example .env
echo "⚠️ Edit .env with your database credentials"

# Create results directory if empty
echo "📁 Creating results directory..."
mkdir -p results

# Verify directory structure
echo "✅ Verifying directory structure..."
directories=("agent" "kb/architecture" "kb/domain" "kb/evaluation" "kb/corrections" "eval" "probes" "planning" "utils" "signal" "results" "docs" "scripts")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ Missing: $dir"
    fi
done

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your database credentials"
echo "2. Run: python agent/main.py --help"
echo "3. Join the mob session at [time]"