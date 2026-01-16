"""
GEON Platform - AI Engine Tester
Test content visibility across multiple AI platforms
"""

import asyncio
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class VisibilityResult:
    """Result of visibility test"""
    engine: str
    query: str
    url_cited: bool
    mention_count: int
    mention_context: List[str]
    position_in_response: Optional[int]
    sentiment: str  # positive, neutral, negative
    timestamp: str


class AIEngineTester:
    """
    Test content visibility across AI engines
    Supports: ChatGPT, Claude, Gemini, Perplexity
    """
    
    def __init__(
        self, 
        openai_api_key: str = None,
        anthropic_api_key: str = None,
        google_api_key: str = None,
        perplexity_api_key: str = None
    ):
        """Initialize with API keys for different engines"""
        self.api_keys = {
            'openai': openai_api_key,
            'anthropic': anthropic_api_key,
            'google': google_api_key,
            'perplexity': perplexity_api_key
        }
        self.test_history = []
    
    async def test_visibility_across_engines(
        self, 
        url: str, 
        test_queries: List[str],
        engines: List[str] = None
    ) -> Dict:
        """
        Test URL visibility across multiple AI engines
        """
        if engines is None:
            engines = ['chatgpt', 'claude', 'gemini', 'perplexity']
        
        results = {
            'url': url,
            'test_date': datetime.now().isoformat(),
            'queries_tested': len(test_queries),
            'engines_tested': engines,
            'overall_visibility': {},
            'detailed_results': [],
            'summary': {}
        }
        
        for query in test_queries:
            for engine in engines:
                if self.api_keys.get(self._get_api_key_name(engine)):
                    result = await self._test_single_query(engine, query, url)
                    results['detailed_results'].append(result)
        
        results['summary'] = self._calculate_summary(results['detailed_results'])
        results['overall_visibility'] = self._calculate_overall_visibility(results['detailed_results'])
        
        return results
    
    async def _test_single_query(
        self, 
        engine: str, 
        query: str, 
        target_url: str
    ) -> VisibilityResult:
        """Test a single query on a single engine"""
        try:
            response = await self._query_engine(engine, query)
            
            url_cited = self._check_url_citation(target_url, response)
            mention_count = self._count_mentions(target_url, response)
            mention_contexts = self._extract_mention_contexts(target_url, response)
            position = self._find_position_in_response(target_url, response)
            sentiment = self._analyze_sentiment(mention_contexts)
            
            return VisibilityResult(
                engine=engine,
                query=query,
                url_cited=url_cited,
                mention_count=mention_count,
                mention_context=mention_contexts,
                position_in_response=position,
                sentiment=sentiment,
                timestamp=datetime.now().isoformat()
            )
        except Exception:
            return VisibilityResult(
                engine=engine,
                query=query,
                url_cited=False,
                mention_count=0,
                mention_context=[],
                position_in_response=None,
                sentiment='error',
                timestamp=datetime.now().isoformat()
            )
    
    async def _query_engine(self, engine: str, query: str) -> str:
        """
        Query specific AI engine
        Returns the full text response
        """
        if engine == 'chatgpt':
            return await self._query_chatgpt(query)
        elif engine == 'claude':
            return await self._query_claude(query)
        elif engine == 'gemini':
            return await self._query_gemini(query)
        elif engine == 'perplexity':
            return await self._query_perplexity(query)
        
        return ""
    
    async def _query_chatgpt(self, query: str) -> str:
        """Query ChatGPT via OpenAI API"""
        return ""
    
    async def _query_claude(self, query: str) -> str:
        """Query Claude via Anthropic API"""
        return ""
    
    async def _query_gemini(self, query: str) -> str:
        """Query Gemini via Google API"""
        return ""
    
    async def _query_perplexity(self, query: str) -> str:
        """Query Perplexity API"""
        return ""
    
    def _check_url_citation(self, url: str, response: str) -> bool:
        clean_url = url.replace('https://', '').replace('http://', '').rstrip('/')
        clean_response = response.lower()
        return clean_url.lower() in clean_response
    
    def _count_mentions(self, url: str, response: str) -> int:
        clean_url = url.replace('https://', '').replace('http://', '').rstrip('/')
        return len(re.findall(re.escape(clean_url.lower()), response.lower()))
    
    def _extract_mention_contexts(self, url: str, response: str, context_length: int = 100) -> List[str]:
        contexts = []
        clean_url = url.replace('https://', '').replace('http://', '').rstrip('/')
        
        for match in re.finditer(re.escape(clean_url.lower()), response.lower()):
            start = max(0, match.start() - context_length)
            end = min(len(response), match.end() + context_length)
            context = response[start:end].strip()
            contexts.append(context)
        
        return contexts
    
    def _find_position_in_response(self, url: str, response: str) -> Optional[int]:
        clean_url = url.replace('https://', '').replace('http://', '').rstrip('/')
        match = re.search(re.escape(clean_url.lower()), response.lower())
        return match.start() if match else None
    
    def _analyze_sentiment(self, contexts: List[str]) -> str:
        if not contexts:
            return 'neutral'
        
        positive_words = ['excellent', 'great', 'best', 'recommended', 'leading', 
                         'top', 'outstanding', 'reliable', 'trusted', 'authoritative']
        negative_words = ['poor', 'bad', 'worst', 'unreliable', 'questionable', 
                         'avoid', 'problematic', 'concerning']
        
        combined_context = ' '.join(contexts).lower()
        
        positive_count = sum(1 for word in positive_words if word in combined_context)
        negative_count = sum(1 for word in negative_words if word in combined_context)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_summary(self, results: List[VisibilityResult]) -> Dict:
        if not results:
            return {}
        
        total_queries = len(results)
        cited_count = sum(1 for r in results if r.url_cited)
        total_mentions = sum(r.mention_count for r in results)
        
        engine_stats = {}
        for result in results:
            if result.engine not in engine_stats:
                engine_stats[result.engine] = {
                    'queries': 0,
                    'citations': 0,
                    'mentions': 0
                }
            
            engine_stats[result.engine]['queries'] += 1
            if result.url_cited:
                engine_stats[result.engine]['citations'] += 1
            engine_stats[result.engine]['mentions'] += result.mention_count
        
        for engine in engine_stats:
            queries = engine_stats[engine]['queries']
            citations = engine_stats[engine]['citations']
            engine_stats[engine]['citation_rate'] = (citations / queries * 100) if queries > 0 else 0
        
        return {
            'total_queries': total_queries,
            'total_citations': cited_count,
            'citation_rate': (cited_count / total_queries * 100) if total_queries > 0 else 0,
            'total_mentions': total_mentions,
            'avg_mentions_per_citation': (total_mentions / cited_count) if cited_count > 0 else 0,
            'engine_statistics': engine_stats
        }
    
    def _calculate_overall_visibility(self, results: List[VisibilityResult]) -> Dict:
        if not results:
            return {'score': 0, 'grade': 'F'}
        
        citation_rate = sum(1 for r in results if r.url_cited) / len(results)
        avg_position = sum(r.position_in_response or 1000 for r in results) / len(results)
        sentiment_score = sum(1 for r in results if r.sentiment == 'positive') / len(results)
        
        position_score = max(0, 1 - (avg_position / 1000))
        
        overall = (
            citation_rate * 40 +
            position_score * 30 +
            sentiment_score * 30
        ) * 100
        
        if overall >= 80: grade = 'A'
        elif overall >= 70: grade = 'B'
        elif overall >= 60: grade = 'C'
        elif overall >= 50: grade = 'D'
        else: grade = 'F'
        
        return {
            'score': round(overall, 1),
            'grade': grade,
            'citation_rate': round(citation_rate * 100, 1),
            'avg_position': round(avg_position, 0),
            'sentiment': 'positive' if sentiment_score > 0.5 else 'neutral'
        }
    
    def _get_api_key_name(self, engine: str) -> str:
        mapping = {
            'chatgpt': 'openai',
            'claude': 'anthropic',
            'gemini': 'google',
            'perplexity': 'perplexity'
        }
        return mapping.get(engine, engine)
    
    def generate_test_queries(self, topic: str, brand_name: str = None) -> List[str]:
        queries = [
            f"What is {topic}?",
            f"Best practices for {topic}",
            f"How to implement {topic}",
            f"{topic} guide",
            f"{topic} explained with examples",
            f"Latest trends in {topic}",
            f"{topic} vs alternatives",
            f"Benefits of {topic}",
            f"{topic} statistics and data",
            f"Expert opinions on {topic}"
        ]
        
        if brand_name:
            queries.extend([
                f"{brand_name} {topic}",
                f"What does {brand_name} say about {topic}?",
                f"{brand_name} approach to {topic}"
            ])
        
        return queries


if __name__ == "__main__":
    async def main():
        tester = AIEngineTester(
            openai_api_key="your-openai-key",
            anthropic_api_key="your-anthropic-key",
            google_api_key="your-google-key"
        )
        
        queries = tester.generate_test_queries(
            topic="generative engine optimization",
            brand_name="GEON"
        )
        
        results = await tester.test_visibility_across_engines(
            url="https://geon.vision",
            test_queries=queries[:5],
            engines=['chatgpt', 'claude', 'gemini']
        )
        
        print("=== AI VISIBILITY TEST RESULTS ===\n")
        print(f"Overall Visibility Score: {results['overall_visibility']['score']}/100")
        print(f"Grade: {results['overall_visibility']['grade']}")
        print(f"\nCitation Rate: {results['summary']['citation_rate']:.1f}%")
        print(f"Total Mentions: {results['summary']['total_mentions']}")
        
        print("\n=== Engine Performance ===")
        for engine, stats in results['summary']['engine_statistics'].items():
            print(f"\n{engine.upper()}:")
            print(f"  Citation Rate: {stats['citation_rate']:.1f}%")
            print(f"  Total Mentions: {stats['mentions']}")
    
    asyncio.run(main())
