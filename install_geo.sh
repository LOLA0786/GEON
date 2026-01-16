#!/bin/bash
set -e

################################################################################
# GEON GEO Enhancement - Complete Installation Script (REPO MODE)
# Works when you cloned https://github.com/LOLA0786/GEON
# Run this in your GEON repo root directory: ~/Geon/GEON
################################################################################

echo "======================================================================"
echo "🎯 GEON GEO Enhancement Installation (Repo Mode)"
echo "======================================================================"
echo ""
echo "✅ This installs GEO features WITHOUT breaking your live app"
echo "Press ENTER to continue or Ctrl+C to cancel"
read

# ----------------------------------------------------------------------
# Step 0: Validate location
# ----------------------------------------------------------------------
echo ""
echo "📍 Step 0: Validating repo..."
if [ ! -f "streamli_main.py" ] && [ ! -f "Readme.Md" ]; then
  echo "❌ ERROR: Run this inside your GEON repo root (example: ~/Geon/GEON)"
  echo "Current dir: $(pwd)"
  exit 1
fi
echo "✅ Repo detected: $(pwd)"

# ----------------------------------------------------------------------
# Step 1: Create geo directory
# ----------------------------------------------------------------------
echo ""
echo "📁 Step 1: Creating geo directory..."
mkdir -p geo
echo "✅ Created: geo/"

# ----------------------------------------------------------------------
# Step 2: Create geo/__init__.py (SAFE IMPORTS)
# ----------------------------------------------------------------------
echo ""
echo "📝 Step 2: Creating geo/__init__.py (safe imports)..."
cat > geo/__init__.py << 'EOF_INNER'
"""
GEON GEO Module
Generative Engine Optimization Tools
"""

__version__ = '1.0.0'

__all__ = []

# SAFE imports: do not crash if any file is missing
try:
    from .analyzer import GEOAnalyzer, GEOScore
    __all__ += ['GEOAnalyzer', 'GEOScore']
except Exception:
    pass

try:
    from .optimizer import GEOOptimizer, Industry, OptimizationPlan
    __all__ += ['GEOOptimizer', 'Industry', 'OptimizationPlan']
except Exception:
    pass

try:
    from .ai_tester import AIEngineTester, VisibilityResult
    __all__ += ['AIEngineTester', 'VisibilityResult']
except Exception:
    pass

try:
    from .serp_tracker import AISERPTracker, CitationRecord, VisibilityStats
    __all__ += ['AISERPTracker', 'CitationRecord', 'VisibilityStats']
except Exception:
    pass
EOF_INNER
echo "✅ Created: geo/__init__.py"

# ----------------------------------------------------------------------
# Step 3: Create geo/models.py
# ----------------------------------------------------------------------
echo ""
echo "📝 Step 3: Creating geo/models.py (data models)..."
cat > geo/models.py << 'EOF_INNER'
"""
GEO Data Models
"""

from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class GEOScore:
    entity_recognition: float
    answer_optimization: float
    semantic_depth: float
    structured_data: float
    authority_signals: float
    citation_worthiness: float
    overall_score: float

@dataclass
class OptimizationPlan:
    primary_methods: List[Dict]
    secondary_methods: List[Dict]
    content_additions: List[str]
    schema_recommendations: List[Dict]
    estimated_improvement: str
    priority_order: List[str]

@dataclass
class VisibilityResult:
    engine: str
    query: str
    url_cited: bool
    mention_count: int
    mention_context: List[str]
    position_in_response: Optional[int]
    sentiment: str
    timestamp: str
EOF_INNER
echo "✅ Created: geo/models.py"

# ----------------------------------------------------------------------
# Step 4: Ensure GEO module files exist (repo mode)
# ----------------------------------------------------------------------
echo ""
echo "======================================================================"
echo "📥 Step 4: Validating GEO module files already in repo"
echo "======================================================================"
echo ""

REQUIRED_FILES=("geo/analyzer.py" "geo/optimizer.py" "geo/ai_tester.py" "geo_quickstart.py")
MISSING=0

for f in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "❌ Missing: $f"
    MISSING=1
  else
    echo "✅ Found: $f"
  fi
done

if [ $MISSING -eq 1 ]; then
  echo ""
  echo "❌ ERROR: Missing required files."
  echo "Fix by creating those files first (we already created them earlier)."
  exit 1
fi

# ----------------------------------------------------------------------
# Step 5: Setup python venv (prevents disk from exploding)
# ----------------------------------------------------------------------
echo ""
echo "======================================================================"
echo "🐍 Step 5: Setup Python virtualenv (.venv)"
echo "======================================================================"
echo ""

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "✅ Created .venv"
else
  echo "ℹ️  .venv already exists"
fi

# Activate
source .venv/bin/activate

# ----------------------------------------------------------------------
# Step 6: Install dependencies into venv
# ----------------------------------------------------------------------
echo ""
echo "======================================================================"
echo "📦 Step 6: Installing dependencies inside venv"
echo "======================================================================"
echo ""

pip install --upgrade pip

cat > requirements_geo.txt << 'EOF_INNER'
streamlit>=1.30.0
plotly>=5.0.0
pandas>=2.0.0
pydantic>=2.0.0
aiohttp>=3.9.0

# optional (only needed when enabling real AI APIs later):
# anthropic>=0.18.0
# openai>=1.0.0
# google-generativeai
EOF_INNER

pip install -r requirements_geo.txt

echo "✅ Dependencies installed"

# ----------------------------------------------------------------------
# Step 7: Create .env template if missing
# ----------------------------------------------------------------------
echo ""
echo "📝 Step 7: Setting up environment variables..."

if [ ! -f .env ]; then
    cat > .env << 'EOF_INNER'
# GEO Feature Flags
ENABLE_GEO=1
ENABLE_REAL_AI_TRACKING=0

# Existing API Key (if used)
GEMINI_API_KEY=

# New GEO API Keys (optional)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
PERPLEXITY_API_KEY=
EOF_INNER
    echo "✅ Created: .env (template)"
    echo "⚠️  IMPORTANT: Add keys only if needed."
else
    echo "ℹ️  .env already exists (not overwriting)"
fi

# ----------------------------------------------------------------------
# Step 8: Test imports
# ----------------------------------------------------------------------
echo ""
echo "======================================================================"
echo "🧪 Step 8: Testing installation imports"
echo "======================================================================"
echo ""

python3 << 'PYEOF'
from geo.analyzer import GEOAnalyzer
from geo.optimizer import GEOOptimizer, Industry
from geo.ai_tester import AIEngineTester

print("✅ Analyzer import OK:", GEOAnalyzer)
print("✅ Optimizer import OK:", GEOOptimizer, Industry)
print("✅ AI Tester import OK:", AIEngineTester)

try:
    from geo.serp_tracker import AISERPTracker
    print("✅ SERP Tracker import OK:", AISERPTracker)
except Exception as e:
    print("ℹ️  SERP tracker not present yet (optional):", e)

print("\n🎉 Installation test PASSED!")
PYEOF

# ----------------------------------------------------------------------
# Step 9: Create test script
# ----------------------------------------------------------------------
echo ""
echo "📝 Step 9: Creating test_geo.py..."
cat > test_geo.py << 'EOF_INNER'
"""
Quick test script for GEO features
Run with: python3 test_geo.py
"""

from geo.analyzer import GEOAnalyzer
from geo.optimizer import GEOOptimizer, Industry

def main():
    analyzer = GEOAnalyzer()
    optimizer = GEOOptimizer()

    sample_html = """
    <html><body>
    <h1>Generative Engine Optimization</h1>
    <p>GEO improves AI visibility by helping models cite your content.</p>
    <p>According to Princeton research, GEO can boost visibility by up to 37%.</p>
    <ul><li>Stats</li><li>Quotes</li><li>Citations</li></ul>
    </body></html>
    """

    results = analyzer.analyze_content(sample_html, "https://example.com")
    print("✅ Analyzer worked. Score:", results["scores"]["overall_score"])

    plan = optimizer.generate_optimization_plan(
        content="GEO is important for modern businesses.",
        industry=Industry.BUSINESS_FINANCE
    )
    print("✅ Optimizer worked. Estimated:", plan.estimated_improvement)

if __name__ == "__main__":
    main()
EOF_INNER

echo "✅ Created: test_geo.py"

# ----------------------------------------------------------------------
# Step 10: Run tests
# ----------------------------------------------------------------------
echo ""
echo "======================================================================"
echo "🧪 Step 10: Running test_geo.py"
echo "======================================================================"
echo ""

python3 test_geo.py

# ----------------------------------------------------------------------
# Final
# ----------------------------------------------------------------------
echo ""
echo "======================================================================"
echo "✅ INSTALLATION COMPLETE!"
echo "======================================================================"
echo ""
echo "🚀 Run quick start:"
echo "   source .venv/bin/activate"
echo "   streamlit run geo_quickstart.py"
echo ""
echo "🧪 Run tests again:"
echo "   python3 test_geo.py"
echo ""
