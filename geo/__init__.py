"""
GEON GEO Module
Generative Engine Optimization Tools
"""

__version__ = "1.0.0"

__all__ = []

# Safe optional imports so partial installs don’t break the whole package
try:
    from .analyzer import GEOAnalyzer, GEOScore
    __all__ += ["GEOAnalyzer", "GEOScore"]
except Exception:
    pass

try:
    from .optimizer import GEOOptimizer, Industry, OptimizationPlan
    __all__ += ["GEOOptimizer", "Industry", "OptimizationPlan"]
except Exception:
    pass

try:
    from .ai_tester import AIEngineTester, VisibilityResult
    __all__ += ["AIEngineTester", "VisibilityResult"]
except Exception:
    pass
