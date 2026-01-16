"""
GEON Platform - GEO Analyzer Module
Analyzes web content for Generative Engine Optimization factors
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json


@dataclass
class GEOScore:
    """GEO scoring metrics"""
    entity_recognition: float  # 0-100
    answer_optimization: float  # 0-100
    semantic_depth: float  # 0-100
    structured_data: float  # 0-100
    authority_signals: float  # 0-100
    citation_worthiness: float  # 0-100
    overall_score: float  # 0-100
    

class GEOAnalyzer:
    """
    Comprehensive GEO Analysis Engine
    Evaluates content for AI visibility and provides actionable insights
    """
    
    def __init__(self, gemini_api_key: str = None):
        """Initialize GEO Analyzer with optional Gemini API key"""
        self.api_key = gemini_api_key
        self.min_content_length = 300  # Minimum content length for analysis
        
    def analyze_content(self, html_content: str, url: str = None) -> Dict:
        """
        Main analysis function - comprehensive GEO evaluation
        
        Args:
            html_content: Raw HTML or cleaned text content
            url: Optional URL for context
            
        Returns:
            Dictionary with scores, recommendations, and detailed analysis
        """
        # Clean and prepare content
        text_content = self._clean_content(html_content)
        
        if len(text_content) < self.min_content_length:
            return {
                'error': 'Content too short for analysis',
                'min_length': self.min_content_length
            }
        
        # Run all analysis components
        scores = self._calculate_all_scores(text_content, html_content)
        recommendations = self._generate_recommendations(scores, text_content)
        opportunities = self._identify_opportunities(text_content, html_content)
        
        return {
            'url': url,
            'scores': scores.__dict__,
            'overall_grade': self._get_grade(scores.overall_score),
            'recommendations': recommendations,
            'opportunities': opportunities,
            'detailed_analysis': {
                'content_length': len(text_content),
                'word_count': len(text_content.split()),
                'paragraph_count': text_content.count('\n\n') + 1,
                'has_structured_data': self._has_schema_markup(html_content),
                'detected_entities': self._extract_entities(text_content)[:10]
            }
        }
    
    def _calculate_all_scores(self, text: str, html: str) -> GEOScore:
        """Calculate all GEO scores"""
        entity_score = self._calculate_entity_score(text)
        answer_score = self._evaluate_answer_format(text)
        semantic_score = self._measure_semantic_coverage(text)
        structured_score = self._check_structured_data(html)
        authority_score = self._identify_authority_signals(text, html)
        citation_score = self._assess_citation_potential(text)
        
        overall = (
            entity_score * 0.2 +
            answer_score * 0.2 +
            semantic_score * 0.15 +
            structured_score * 0.15 +
            authority_score * 0.15 +
            citation_score * 0.15
        )
        
        return GEOScore(
            entity_recognition=entity_score,
            answer_optimization=answer_score,
            semantic_depth=semantic_score,
            structured_data=structured_score,
            authority_signals=authority_score,
            citation_worthiness=citation_score,
            overall_score=overall
        )
    
    def _calculate_entity_score(self, text: str) -> float:
        """
        Score based on entity recognition potential
        Checks for proper nouns, organizations, locations, etc.
        """
        score = 0.0
        
        # Check for capitalized entities (basic NER)
        capitalized_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entity_density = len(capitalized_words) / max(len(text.split()), 1)
        
        # Optimal entity density: 5-15%
        if 0.05 <= entity_density <= 0.15:
            score += 50
        elif entity_density > 0:
            score += min(entity_density * 300, 50)
        
        # Check for specific entity types
        has_numbers = bool(re.search(r'\d+', text))
        has_dates = bool(re.search(r'\b\d{4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b', text))
        has_organizations = bool(re.search(r'\b(?:Inc|LLC|Ltd|Corp|Company|Organization)\b', text, re.IGNORECASE))
        
        if has_numbers: score += 15
        if has_dates: score += 15
        if has_organizations: score += 20
        
        return min(score, 100)
    
    def _evaluate_answer_format(self, text: str) -> float:
        """
        Evaluate how well content is formatted for direct answers
        AI engines prefer answer-first, clear formatting
        """
        score = 0.0
        
        # Check for question-answer format
        questions = re.findall(r'\?', text)
        if len(questions) > 0:
            score += 20
        
        # Check for list formats (numbered or bulleted)
        has_lists = bool(re.search(r'(?:^|\n)\s*(?:\d+\.|\*|\-)\s+', text, re.MULTILINE))
        if has_lists:
            score += 25
        
        # Check for definition patterns
        definition_patterns = [
            r'\b(?:is|are|means|refers to|defined as)\b',
            r'\b(?:In other words|Simply put|Essentially)\b',
        ]
        for pattern in definition_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 15
                break
        
        # Check for clear structure (headings, sections)
        paragraphs = text.split('\n\n')
        if 3 <= len(paragraphs) <= 20:  # Optimal paragraph count
            score += 20
        
        # Check for concise opening
        first_para = paragraphs[0] if paragraphs else ""
        if 50 <= len(first_para.split()) <= 100:  # Ideal opening length
            score += 20
        
        return min(score, 100)
    
    def _measure_semantic_coverage(self, text: str) -> float:
        """
        Measure semantic richness and topic coverage
        """
        score = 0.0
        words = text.lower().split()
        unique_words = set(words)
        
        # Vocabulary diversity
        vocab_diversity = len(unique_words) / max(len(words), 1)
        if vocab_diversity >= 0.5:  # Good diversity
            score += 30
        else:
            score += vocab_diversity * 60
        
        # Check for explanatory phrases
        explanatory_phrases = [
            'for example', 'such as', 'including', 'specifically',
            'in particular', 'namely', 'that is', 'i.e.', 'e.g.'
        ]
        explanations_found = sum(1 for phrase in explanatory_phrases if phrase in text.lower())
        score += min(explanations_found * 10, 30)
        
        # Check for comparative language
        comparative_words = ['compared to', 'versus', 'unlike', 'similar to', 'different from']
        comparisons_found = sum(1 for word in comparative_words if word in text.lower())
        score += min(comparisons_found * 10, 20)
        
        # Check for technical depth (longer words = more technical)
        avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
        if avg_word_length >= 5:  # Technical content
            score += 20
        
        return min(score, 100)
    
    def _check_structured_data(self, html: str) -> float:
        """
        Check for structured data (Schema.org, JSON-LD, microdata)
        """
        score = 0.0
        
        # Check for JSON-LD
        if '<script type="application/ld+json">' in html:
            score += 40
        
        # Check for Schema.org microdata
        if 'itemscope' in html or 'itemtype' in html:
            score += 30
        
        # Check for Open Graph tags
        if 'og:' in html:
            score += 15
        
        # Check for Twitter Card tags
        if 'twitter:' in html:
            score += 15
        
        return min(score, 100)
    
    def _identify_authority_signals(self, text: str, html: str) -> float:
        """
        Identify authority and trust signals
        """
        score = 0.0
        
        # Check for author attribution
        author_patterns = [
            r'\bby\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # "by John Doe"
            r'\bwritten by\b',
            r'\bauthor:?\b',
        ]
        for pattern in author_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 20
                break
        
        # Check for citations/references
        if re.search(r'\[(\d+)\]|\(\d{4}\)|et al\.|according to', text, re.IGNORECASE):
            score += 25
        
        # Check for statistics and data
        has_percentages = bool(re.search(r'\d+%', text))
        has_numbers = bool(re.search(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text))
        
        if has_percentages: score += 15
        if has_numbers: score += 15
        
        # Check for expertise indicators
        expertise_terms = ['research', 'study', 'analysis', 'expert', 'professor', 'phd', 'dr.']
        expertise_found = sum(1 for term in expertise_terms if term in text.lower())
        score += min(expertise_found * 5, 25)
        
        return min(score, 100)
    
    def _assess_citation_potential(self, text: str) -> float:
        """
        Assess how likely content is to be cited by AI
        """
        score = 0.0
        
        # Factual content indicators
        factual_markers = ['according to', 'research shows', 'studies indicate', 
                          'data reveals', 'statistics show', 'analysis suggests']
        factual_count = sum(1 for marker in factual_markers if marker in text.lower())
        score += min(factual_count * 15, 40)
        
        # Quotable statements (short, clear sentences)
        sentences = re.split(r'[.!?]+', text)
        quotable_sentences = [s for s in sentences if 10 <= len(s.split()) <= 25]
        score += min(len(quotable_sentences) * 2, 30)
        
        # Unique insights (using power words)
        insight_words = ['importantly', 'notably', 'significantly', 'surprisingly', 
                        'interestingly', 'key finding', 'main takeaway']
        insights = sum(1 for word in insight_words if word in text.lower())
        score += min(insights * 10, 30)
        
        return min(score, 100)
    
    def _generate_recommendations(self, scores: GEOScore, text: str) -> List[Dict]:
        """Generate prioritized recommendations based on scores"""
        recommendations = []
        
        # Entity Recognition recommendations
        if scores.entity_recognition < 60:
            recommendations.append({
                'category': 'Entity Recognition',
                'priority': 'HIGH',
                'action': 'Add more named entities (people, places, organizations)',
                'impact': 'Improves AI understanding of content context',
                'examples': [
                    'Include specific company names, products, or locations',
                    'Add dates and numerical data',
                    'Reference industry leaders or experts'
                ]
            })
        
        # Answer Format recommendations
        if scores.answer_optimization < 60:
            recommendations.append({
                'category': 'Answer Format',
                'priority': 'HIGH',
                'action': 'Restructure content for direct answers',
                'impact': 'Makes content easier for AI to extract and cite',
                'examples': [
                    'Start with a clear, concise answer (50-100 words)',
                    'Use FAQ format for common questions',
                    'Add TL;DR or summary sections',
                    'Include bulleted or numbered lists'
                ]
            })
        
        # Semantic Depth recommendations
        if scores.semantic_depth < 60:
            recommendations.append({
                'category': 'Semantic Coverage',
                'priority': 'MEDIUM',
                'action': 'Expand topic coverage and depth',
                'impact': 'Increases relevance for diverse queries',
                'examples': [
                    'Add explanatory examples ("for example", "such as")',
                    'Include comparisons and contrasts',
                    'Cover related subtopics',
                    'Use varied vocabulary'
                ]
            })
        
        # Structured Data recommendations
        if scores.structured_data < 60:
            recommendations.append({
                'category': 'Structured Data',
                'priority': 'HIGH',
                'action': 'Implement Schema.org markup',
                'impact': 'Critical for AI engines to understand content',
                'examples': [
                    'Add JSON-LD schema for articles',
                    'Implement FAQ schema for Q&A content',
                    'Add Organization schema for company info',
                    'Include breadcrumb schema for navigation'
                ]
            })
        
        # Authority Signals recommendations
        if scores.authority_signals < 60:
            recommendations.append({
                'category': 'Authority Signals',
                'priority': 'MEDIUM',
                'action': 'Strengthen credibility indicators',
                'impact': 'Builds trust with AI engines',
                'examples': [
                    'Add author bios with credentials',
                    'Include data and statistics',
                    'Cite authoritative sources',
                    'Add publication dates and update timestamps'
                ]
            })
        
        # Citation Worthiness recommendations
        if scores.citation_worthiness < 60:
            recommendations.append({
                'category': 'Citation Worthiness',
                'priority': 'MEDIUM',
                'action': 'Make content more quotable',
                'impact': 'Increases likelihood of AI citation',
                'examples': [
                    'Add clear, factual statements (10-25 words)',
                    'Include unique insights or findings',
                    'Use authoritative language',
                    'Provide specific data points'
                ]
            })
        
        return sorted(recommendations, key=lambda x: {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[x['priority']], reverse=True)
    
    def _identify_opportunities(self, text: str, html: str) -> Dict:
        """Identify specific GEO opportunities"""
        opportunities = {
            'quick_wins': [],
            'medium_effort': [],
            'long_term': []
        }
        
        # Quick wins
        if not self._has_schema_markup(html):
            opportunities['quick_wins'].append({
                'opportunity': 'Add JSON-LD Schema',
                'estimated_time': '30 minutes',
                'impact': 'High - Immediate AI comprehension boost'
            })
        
        if not re.search(r'\?', text):
            opportunities['quick_wins'].append({
                'opportunity': 'Add FAQ section',
                'estimated_time': '1 hour',
                'impact': 'High - Direct answer optimization'
            })
        
        # Medium effort
        if len(re.findall(r'\d+%', text)) < 3:
            opportunities['medium_effort'].append({
                'opportunity': 'Add statistics and data points',
                'estimated_time': '2-3 hours',
                'impact': 'Medium - Increases authority and citation potential'
            })
        
        # Long term
        opportunities['long_term'].append({
            'opportunity': 'Build topical authority cluster',
                'estimated_time': '1-2 weeks',
                'impact': 'Very High - Comprehensive topic coverage'
            })
        
        return opportunities
    
    def _clean_content(self, html_or_text: str) -> str:
        """Clean HTML or text content"""
        # Remove HTML tags
        text = re.sub(r'<script[^>]*>.*?</script>', '', html_or_text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def _has_schema_markup(self, html: str) -> bool:
        """Check if HTML contains any schema markup"""
        return any([
            '<script type="application/ld+json">' in html,
            'itemscope' in html,
            'itemtype' in html,
            '"@context"' in html
        ])
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract potential named entities"""
        # Simple entity extraction (capitalized phrases)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return list(set(entities))  # Remove duplicates
    
    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90: return 'A+'
        elif score >= 85: return 'A'
        elif score >= 80: return 'A-'
        elif score >= 75: return 'B+'
        elif score >= 70: return 'B'
        elif score >= 65: return 'B-'
        elif score >= 60: return 'C+'
        elif score >= 55: return 'C'
        elif score >= 50: return 'C-'
        else: return 'F'


# Usage example
if __name__ == "__main__":
    analyzer = GEOAnalyzer()
    
    sample_html = """
    <html>
    <head>
        <title>Sample Article</title>
        <meta property="og:title" content="Sample Article">
    </head>
    <body>
        <h1>Understanding Generative Engine Optimization</h1>
        <p>Generative Engine Optimization (GEO) is a modern approach to digital visibility. 
        According to research from Princeton University, GEO can improve visibility by up to 37%.</p>
        
        <h2>Key Benefits</h2>
        <ul>
            <li>Increased AI citation frequency</li>
            <li>Better brand visibility in ChatGPT and Claude</li>
            <li>Higher authority scores</li>
        </ul>
        
        <p>Expert Dr. Jane Smith notes, "GEO represents the future of search optimization."</p>
    </body>
    </html>
    """
    
    results = analyzer.analyze_content(sample_html, "https://example.com/article")
    print(json.dumps(results, indent=2))
