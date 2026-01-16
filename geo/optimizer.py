"""
GEON Platform - GEO Optimizer Module
Generates specific optimization strategies based on GEO research
Based on Princeton's GEO paper and industry best practices
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class GEOMethod(Enum):
    """GEO optimization methods from research"""
    STATISTICS_ADDITION = "statistics_addition"
    QUOTATION_ADDITION = "quotation_addition"
    CITE_SOURCES = "cite_sources"
    FLUENCY_OPTIMIZATION = "fluency_optimization"
    AUTHORITATIVE_WRITING = "authoritative_writing"
    TECHNICAL_TERMS = "technical_terms"
    UNIQUE_WORDS = "unique_words"
    EEAT_ENHANCEMENT = "eeat_enhancement"


class Industry(Enum):
    """Industry categories for tailored recommendations"""
    SCIENCE_TECH = "science_tech"
    BUSINESS_FINANCE = "business_finance"
    ARTS_HUMANITIES = "arts_humanities"
    HEALTH_MEDICAL = "health_medical"
    LEGAL = "legal"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    GENERAL = "general"


@dataclass
class OptimizationPlan:
    """Structured optimization plan"""
    primary_methods: List[Dict]
    secondary_methods: List[Dict]
    content_additions: List[str]
    schema_recommendations: List[Dict]
    estimated_improvement: str
    priority_order: List[str]


class GEOOptimizer:
    """
    Advanced GEO Optimization Engine
    Generates actionable optimization strategies
    """
    
    # Performance data from Princeton GEO research
    METHOD_PERFORMANCE = {
        GEOMethod.STATISTICS_ADDITION: {
            'improvement': 22,  # 22% improvement on Position-Adjusted Word Count
            'difficulty': 'MEDIUM',
            'time_investment': '2-4 hours'
        },
        GEOMethod.QUOTATION_ADDITION: {
            'improvement': 37,  # 37% improvement on Subjective Impression
            'difficulty': 'MEDIUM',
            'time_investment': '2-3 hours'
        },
        GEOMethod.CITE_SOURCES: {
            'improvement': 115,  # 115% increase for 5th ranked sites
            'difficulty': 'LOW',
            'time_investment': '1-2 hours'
        },
        GEOMethod.FLUENCY_OPTIMIZATION: {
            'improvement': 15,
            'difficulty': 'LOW',
            'time_investment': '1 hour'
        },
        GEOMethod.AUTHORITATIVE_WRITING: {
            'improvement': 20,
            'difficulty': 'MEDIUM',
            'time_investment': '3-5 hours'
        },
        GEOMethod.TECHNICAL_TERMS: {
            'improvement': 18,
            'difficulty': 'MEDIUM',
            'time_investment': '2-3 hours'
        },
        GEOMethod.UNIQUE_WORDS: {
            'improvement': 12,
            'difficulty': 'LOW',
            'time_investment': '1-2 hours'
        },
        GEOMethod.EEAT_ENHANCEMENT: {
            'improvement': 25,
            'difficulty': 'HIGH',
            'time_investment': '5-10 hours'
        }
    }
    
    # Industry-specific optimization strategies
    INDUSTRY_STRATEGIES = {
        Industry.SCIENCE_TECH: [
            GEOMethod.TECHNICAL_TERMS,
            GEOMethod.STATISTICS_ADDITION,
            GEOMethod.CITE_SOURCES,
            GEOMethod.AUTHORITATIVE_WRITING
        ],
        Industry.BUSINESS_FINANCE: [
            GEOMethod.STATISTICS_ADDITION,
            GEOMethod.CITE_SOURCES,
            GEOMethod.QUOTATION_ADDITION,
            GEOMethod.EEAT_ENHANCEMENT
        ],
        Industry.ARTS_HUMANITIES: [
            GEOMethod.QUOTATION_ADDITION,
            GEOMethod.CITE_SOURCES,
            GEOMethod.UNIQUE_WORDS,
            GEOMethod.FLUENCY_OPTIMIZATION
        ],
        Industry.HEALTH_MEDICAL: [
            GEOMethod.CITE_SOURCES,
            GEOMethod.EEAT_ENHANCEMENT,
            GEOMethod.STATISTICS_ADDITION,
            GEOMethod.AUTHORITATIVE_WRITING
        ],
        Industry.LEGAL: [
            GEOMethod.CITE_SOURCES,
            GEOMethod.AUTHORITATIVE_WRITING,
            GEOMethod.TECHNICAL_TERMS,
            GEOMethod.EEAT_ENHANCEMENT
        ],
        Industry.ECOMMERCE: [
            GEOMethod.STATISTICS_ADDITION,
            GEOMethod.QUOTATION_ADDITION,
            GEOMethod.CITE_SOURCES,
            GEOMethod.UNIQUE_WORDS
        ],
        Industry.EDUCATION: [
            GEOMethod.CITE_SOURCES,
            GEOMethod.QUOTATION_ADDITION,
            GEOMethod.FLUENCY_OPTIMIZATION,
            GEOMethod.STATISTICS_ADDITION
        ],
        Industry.GENERAL: [
            GEOMethod.CITE_SOURCES,
            GEOMethod.STATISTICS_ADDITION,
            GEOMethod.FLUENCY_OPTIMIZATION,
            GEOMethod.QUOTATION_ADDITION
        ]
    }
    
    def __init__(self):
        """Initialize GEO Optimizer"""
        self.schema_templates = self._load_schema_templates()
    
    def generate_optimization_plan(
        self, 
        content: str, 
        industry: Industry = Industry.GENERAL,
        current_scores: Dict = None,
        target_ai_engines: List[str] = None
    ) -> OptimizationPlan:
        """
        Generate comprehensive optimization plan
        """
        primary_methods = self._get_primary_methods(industry, current_scores)
        secondary_methods = self._get_secondary_methods(industry, current_scores)
        
        content_additions = self._generate_content_additions(
            content, 
            primary_methods, 
            industry
        )
        
        schema_recommendations = self._generate_schema_recommendations(content, industry)
        estimated_improvement = self._calculate_expected_improvement(primary_methods)
        
        priority_order = self._determine_priority_order(
            primary_methods, 
            secondary_methods,
            current_scores
        )
        
        return OptimizationPlan(
            primary_methods=primary_methods,
            secondary_methods=secondary_methods,
            content_additions=content_additions,
            schema_recommendations=schema_recommendations,
            estimated_improvement=estimated_improvement,
            priority_order=priority_order
        )
    
    def _get_primary_methods(self, industry: Industry, scores: Dict = None) -> List[Dict]:
        methods = self.INDUSTRY_STRATEGIES.get(industry, self.INDUSTRY_STRATEGIES[Industry.GENERAL])
        
        primary = []
        for method in methods[:3]:
            method_data = self.METHOD_PERFORMANCE[method].copy()
            method_data['method'] = method.value
            method_data['details'] = self._get_method_details(method, industry)
            primary.append(method_data)
        
        return primary
    
    def _get_secondary_methods(self, industry: Industry, scores: Dict = None) -> List[Dict]:
        methods = self.INDUSTRY_STRATEGIES.get(industry, self.INDUSTRY_STRATEGIES[Industry.GENERAL])
        
        secondary = []
        for method in methods[3:]:
            method_data = self.METHOD_PERFORMANCE[method].copy()
            method_data['method'] = method.value
            method_data['details'] = self._get_method_details(method, industry)
            secondary.append(method_data)
        
        return secondary
    
    def _get_method_details(self, method: GEOMethod, industry: Industry) -> Dict:
        details = {
            GEOMethod.STATISTICS_ADDITION: {
                'description': 'Add relevant statistics and data points to support claims',
                'implementation': [
                    'Identify claims that need statistical support',
                    'Research authoritative sources for data',
                    'Add specific numbers, percentages, and metrics',
                    'Include date ranges and sample sizes',
                    'Cite data sources properly'
                ],
                'examples': [
                    '"According to [Source], 67% of businesses report..."',
                    '"Market research shows a 45% increase from 2023 to 2024"',
                    '"In a study of 1,000 participants, researchers found..."'
                ],
                'ai_impact': 'Statistics significantly improve citation worthiness and authority'
            },
            GEOMethod.QUOTATION_ADDITION: {
                'description': 'Include expert quotes and authoritative statements',
                'implementation': [
                    'Identify key points needing expert validation',
                    'Find relevant quotes from industry experts',
                    'Include full attribution (name, title, organization)',
                    'Use quotes that are concise and impactful (10-25 words)',
                    'Balance quote quantity (2-4 per 1000 words)'
                ],
                'examples': [
                    '"Dr. Jane Smith, AI researcher at MIT, notes: \'GEO represents a fundamental shift in search\'"',
                    'As CEO John Doe explains, "The future of visibility lies in AI optimization"'
                ],
                'ai_impact': 'Quotes add credibility and create quotable content for AI engines'
            },
            GEOMethod.CITE_SOURCES: {
                'description': 'Properly cite authoritative sources throughout content',
                'implementation': [
                    'Add inline citations for all factual claims',
                    'Link to authoritative sources (edu, gov, established publications)',
                    'Use consistent citation format',
                    'Include publication dates',
                    'Add reference section if appropriate'
                ],
                'examples': [
                    '[1] Princeton University (2023). "Generative Engine Optimization"',
                    'According to research from MIT [2]...',
                    'Source: Harvard Business Review, January 2024'
                ],
                'ai_impact': 'Critical for AI engines to verify and trust information'
            },
            GEOMethod.FLUENCY_OPTIMIZATION: {
                'description': 'Improve readability and natural language flow',
                'implementation': [
                    'Break up long sentences (aim for 15-20 words)',
                    'Use transition words (however, therefore, additionally)',
                    'Vary sentence structure',
                    'Remove jargon or explain technical terms',
                    'Use active voice'
                ],
                'examples': [
                    'Before: "The implementation of GEO methodologies..."',
                    'After: "GEO methods help businesses improve..."'
                ],
                'ai_impact': 'Better fluency improves AI comprehension and extraction'
            },
            GEOMethod.AUTHORITATIVE_WRITING: {
                'description': 'Adopt authoritative, expert tone',
                'implementation': [
                    'Use confident, declarative statements',
                    'Back claims with evidence',
                    'Demonstrate subject matter expertise',
                    'Include technical accuracy',
                    'Avoid hedging language unless appropriate'
                ],
                'examples': [
                    'Instead of: "GEO might help improve..."',
                    'Use: "GEO improves visibility by targeting..."'
                ],
                'ai_impact': 'Authoritative content is more likely to be cited'
            },
            GEOMethod.TECHNICAL_TERMS: {
                'description': 'Include appropriate technical terminology',
                'implementation': [
                    'Use industry-specific terminology',
                    'Define technical terms on first use',
                    'Include acronyms with full forms',
                    'Balance technical depth with accessibility',
                    'Add glossary for complex topics'
                ],
                'examples': [
                    '"Large Language Models (LLMs) use retrieval-augmented generation (RAG)..."',
                    '"The semantic vector space allows for..."'
                ],
                'ai_impact': 'Technical terms improve topical relevance in AI systems'
            },
            GEOMethod.UNIQUE_WORDS: {
                'description': 'Increase vocabulary diversity and unique phrasing',
                'implementation': [
                    'Use varied vocabulary (avoid repetition)',
                    'Include synonyms and related terms',
                    'Add descriptive adjectives',
                    'Use specific nouns instead of generic ones',
                    'Incorporate industry-specific language'
                ],
                'examples': [
                    'Instead of repeating "improve", use: enhance, optimize, boost, elevate',
                    'Instead of "thing", use specific: algorithm, framework, methodology'
                ],
                'ai_impact': 'Unique words expand semantic coverage for diverse queries'
            },
            GEOMethod.EEAT_ENHANCEMENT: {
                'description': 'Improve Experience, Expertise, Authoritativeness, Trust signals',
                'implementation': [
                    'Add detailed author bios with credentials',
                    'Include real-world experience and case studies',
                    'Display certifications and awards',
                    'Add editorial review process info',
                    'Include update dates and version history',
                    'Show company/author accomplishments'
                ],
                'examples': [
                    '"Written by Dr. Sarah Johnson, PhD in Computer Science with 15 years of AI research"',
                    '"Last updated: January 2026 | Reviewed by editorial board"',
                    '"Based on analysis of 500+ GEO implementations"'
                ],
                'ai_impact': 'EEAT is critical for Google\'s AI Overviews and other AI systems'
            }
        }
        
        return details.get(method, {})
    
    def _generate_content_additions(self, content: str, primary_methods: List[Dict], industry: Industry) -> List[str]:
        additions = []
        
        for method_data in primary_methods:
            method = GEOMethod(method_data['method'])
            
            if method == GEOMethod.STATISTICS_ADDITION:
                additions.extend([
                    "📊 Add section: 'Key Statistics and Data'",
                    "Add: Market size, growth rates, adoption percentages",
                    "Include: Year-over-year comparisons",
                    "Cite: Industry reports, government data, research studies"
                ])
            
            elif method == GEOMethod.QUOTATION_ADDITION:
                additions.extend([
                    "💬 Add 2-4 expert quotes from recognized authorities",
                    "Include: Full name, title, organization for each expert",
                    "Format: Keep quotes concise (10-25 words)",
                    "Distribute: One quote per major section"
                ])
            
            elif method == GEOMethod.CITE_SOURCES:
                additions.extend([
                    "📚 Add References section at the end",
                    "Add inline citations: [1], [2], etc.",
                    "Link to: Academic papers, industry publications, official sources",
                    "Include: Publication dates and author names"
                ])
            
            elif method == GEOMethod.EEAT_ENHANCEMENT:
                additions.extend([
                    "👤 Add comprehensive author bio (100-150 words)",
                    "Include: Credentials, experience, notable achievements",
                    "Add: 'Last Updated' and 'Review Date'",
                    "Display: Relevant certifications or awards"
                ])
        
        return additions
    
    def _generate_schema_recommendations(self, content: str, industry: Industry) -> List[Dict]:
        recommendations = []
        
        recommendations.append({
            'type': 'Article',
            'priority': 'HIGH',
            'template': self.schema_templates['article'],
            'fields_to_complete': [
                'headline', 'author', 'datePublished', 'dateModified',
                'description', 'image'
            ]
        })
        
        if '?' in content:
            recommendations.append({
                'type': 'FAQPage',
                'priority': 'HIGH',
                'template': self.schema_templates['faq'],
                'fields_to_complete': [
                    'mainEntity (array of questions/answers)'
                ]
            })
        
        if any(word in content.lower() for word in ['step', 'how to', 'guide', 'tutorial']):
            recommendations.append({
                'type': 'HowTo',
                'priority': 'MEDIUM',
                'template': self.schema_templates['howto'],
                'fields_to_complete': [
                    'name', 'step (array)', 'totalTime', 'tool', 'supply'
                ]
            })
        
        recommendations.append({
            'type': 'Organization',
            'priority': 'MEDIUM',
            'template': self.schema_templates['organization'],
            'fields_to_complete': [
                'name', 'url', 'logo', 'sameAs (social profiles)'
            ]
        })
        
        if industry == Industry.ECOMMERCE:
            recommendations.append({
                'type': 'Product',
                'priority': 'HIGH',
                'template': self.schema_templates['product'],
                'fields_to_complete': [
                    'name', 'image', 'description', 'offers', 'aggregateRating'
                ]
            })
        
        return recommendations
    
    def _load_schema_templates(self) -> Dict:
        return {
            'article': {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": "",
                "author": {
                    "@type": "Person",
                    "name": ""
                },
                "datePublished": "",
                "dateModified": "",
                "description": "",
                "image": ""
            },
            'faq': {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": []
            },
            'howto': {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": "",
                "step": []
            },
            'organization': {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "",
                "url": "",
                "logo": "",
                "sameAs": []
            },
            'product': {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": "",
                "image": "",
                "description": "",
                "offers": {
                    "@type": "Offer",
                    "price": "",
                    "priceCurrency": "USD"
                }
            }
        }
    
    def _calculate_expected_improvement(self, methods: List[Dict]) -> str:
        total = sum(method['improvement'] for method in methods)
        avg = total / len(methods) if methods else 0
        
        if avg >= 30:
            return f"HIGH ({int(avg)}% average improvement expected)"
        elif avg >= 20:
            return f"MEDIUM-HIGH ({int(avg)}% average improvement expected)"
        elif avg >= 10:
            return f"MEDIUM ({int(avg)}% average improvement expected)"
        else:
            return f"LOW-MEDIUM ({int(avg)}% average improvement expected)"
    
    def _determine_priority_order(self, primary: List[Dict], secondary: List[Dict], scores: Dict = None) -> List[str]:
        all_methods = primary + secondary
        difficulty_order = {'LOW': 3, 'MEDIUM': 2, 'HIGH': 1}
        
        sorted_methods = sorted(
            all_methods,
            key=lambda x: (x['improvement'], difficulty_order[x['difficulty']]),
            reverse=True
        )
        
        return [m['method'] for m in sorted_methods]


if __name__ == "__main__":
    optimizer = GEOOptimizer()
    
    sample_content = """
    Generative Engine Optimization is important for modern businesses.
    It helps with visibility in AI search engines. Companies should consider
    implementing GEO strategies to stay competitive.
    """
    
    plan = optimizer.generate_optimization_plan(
        content=sample_content,
        industry=Industry.BUSINESS_FINANCE,
        current_scores={
            'entity_recognition': 45,
            'answer_optimization': 50,
            'citation_worthiness': 40
        }
    )
    
    print("=== GEO OPTIMIZATION PLAN ===\n")
    print(f"Estimated Improvement: {plan.estimated_improvement}\n")
    print("\nPrimary Methods:")
    for method in plan.primary_methods:
        print(f"  - {method['method']}: {method['improvement']}% improvement potential")
    
    print("\nContent Additions:")
    for addition in plan.content_additions[:5]:
        print(f"  {addition}")
    
    print("\nSchema Recommendations:")
    for schema in plan.schema_recommendations:
        print(f"  - {schema['type']} (Priority: {schema['priority']})")
