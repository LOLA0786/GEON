"""
GEO Data Models
"""

from dataclasses import dataclass
from typing import List, Optional


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
    primary_methods: List[dict]
    secondary_methods: List[dict]
    content_additions: List[str]
    schema_recommendations: List[dict]
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
