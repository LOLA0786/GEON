#!/bin/bash
set -e

echo "======================================================================"
echo "🎯 GEON Beast GEO Installer (Repo Mode)"
echo "======================================================================"
echo ""

# Must run inside repo
if [ ! -f "streamli_main.py" ] && [ ! -f "Readme.Md" ]; then
  echo "❌ Run this inside GEON repo root (example: ~/Geon/GEON)"
  exit 1
fi

echo "✅ Repo detected at: $(pwd)"

echo ""
echo "📁 Step 1: Ensure geo/ module exists..."
mkdir -p geo
echo "✅ geo/ ready"

echo ""
echo "🐍 Step 2: Create venv (.venv) to avoid filling ~/.local ..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip

echo ""
echo "📦 Step 3: Install dependencies (inside venv)..."
pip install streamlit plotly pandas pydantic aiohttp

echo ""
echo "🧪 Step 4: Verify GEO modules exist..."
for f in geo/analyzer.py geo/optimizer.py geo/ai_tester.py; do
  if [ ! -f "$f" ]; then
    echo "❌ Missing file: $f"
    echo "Fix it before running installer."
    exit 1
  fi
done
echo "✅ GEO modules found"

echo ""
echo "🧪 Step 5: Test imports..."
python3 - << 'PY'
from geo.analyzer import GEOAnalyzer
from geo.optimizer import GEOOptimizer, Industry
from geo.ai_tester import AIEngineTester
print("✅ Analyzer OK:", GEOAnalyzer)
print("✅ Optimizer OK:", GEOOptimizer, Industry)
print("✅ AI Tester OK:", AIEngineTester)
PY

echo ""
echo "🚀 Step 6: Run quickstart app..."
echo "Opening Streamlit now:"
echo "   streamlit run geo_quickstart.py"
echo ""
streamlit run geo_quickstart.py
