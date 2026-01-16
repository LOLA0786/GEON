"""
GEON Beast Mode - AI SERP Tracker
Track citations across ChatGPT, Claude, Gemini, Perplexity
This feature alone sells $200/mo subscriptions
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import sqlite3


@dataclass
class CitationRecord:
    """Single citation tracking record"""
    timestamp: str
    domain: str
    query: str
    engine: str  # chatgpt, claude, gemini, perplexity
    cited: bool
    position: Optional[int]  # Position in response (1-based)
    competitor_cited: List[str]  # List of competitors cited instead
    response_snippet: str  # First 200 chars of AI response
    visibility_score: float  # 0-100


@dataclass
class VisibilityStats:
    """Aggregated visibility statistics"""
    total_queries: int
    citations_won: int
    citations_lost: int
    citation_rate: float  # Percentage
    avg_position: float
    top_winning_pages: List[Dict]
    top_losing_pages: List[Dict]
    competitor_wins: Dict[str, int]
    visibility_score: float  # 0-100
    trend: str  # "improving", "declining", "stable"


class AISERPTracker:
    """
    AI Search Engine Results Position Tracker
    The #1 feature that justifies $200/mo pricing
    """
    
    def __init__(self, db_path: str = "geo_tracking.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                domain TEXT NOT NULL,
                query TEXT NOT NULL,
                engine TEXT NOT NULL,
                cited INTEGER NOT NULL,
                position INTEGER,
                competitors TEXT,
                response_snippet TEXT,
                visibility_score REAL,
                UNIQUE(timestamp, domain, query, engine)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracked_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                query TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                UNIQUE(domain, query)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                competitor_domain TEXT NOT NULL,
                UNIQUE(domain, competitor_domain)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_tracked_queries(self, domain: str, queries: List[str]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        for query in queries:
            cursor.execute("""
                INSERT OR IGNORE INTO tracked_queries (domain, query, created_at)
                VALUES (?, ?, ?)
            """, (domain, query, timestamp))
        
        conn.commit()
        conn.close()
        return len(queries)
    
    def add_competitors(self, domain: str, competitors: List[str]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for competitor in competitors:
            cursor.execute("""
                INSERT OR IGNORE INTO competitors (domain, competitor_domain)
                VALUES (?, ?)
            """, (domain, competitor))
        
        conn.commit()
        conn.close()
    
    async def run_tracking_cycle(
        self, 
        domain: str,
        engines: List[str] = None,
        api_keys: Dict[str, str] = None
    ) -> Dict:
        if engines is None:
            engines = ['chatgpt', 'claude', 'gemini', 'perplexity']
        
        queries = self._get_tracked_queries(domain)
        competitors = self._get_competitors(domain)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'domain': domain,
            'queries_tested': len(queries),
            'engines_tested': engines,
            'records_created': 0,
            'citations_won': 0,
            'citations_lost': 0
        }
        
        for query in queries:
            for engine in engines:
                record = await self._test_single_query(
                    domain=domain,
                    query=query,
                    engine=engine,
                    competitors=competitors,
                    api_keys=api_keys
                )
                
                self._save_citation_record(record)
                results['records_created'] += 1
                
                if record.cited:
                    results['citations_won'] += 1
                else:
                    results['citations_lost'] += 1
        
        return results
    
    async def _test_single_query(
        self,
        domain: str,
        query: str,
        engine: str,
        competitors: List[str],
        api_keys: Dict[str, str] = None
    ) -> CitationRecord:
        
        response = await self._query_ai_engine(engine, query, api_keys)
        
        cited = self._check_citation(domain, response)
        position = self._find_position(domain, response) if cited else None
        
        competitor_cited = [
            comp for comp in competitors 
            if self._check_citation(comp, response)
        ]
        
        visibility_score = self._calculate_visibility_score(
            cited=cited,
            position=position,
            total_competitors=len(competitors),
            competitors_cited=len(competitor_cited)
        )
        
        return CitationRecord(
            timestamp=datetime.now().isoformat(),
            domain=domain,
            query=query,
            engine=engine,
            cited=cited,
            position=position,
            competitor_cited=competitor_cited,
            response_snippet=response[:200] if response else "",
            visibility_score=visibility_score
        )
    
    async def _query_ai_engine(
        self, 
        engine: str, 
        query: str,
        api_keys: Dict[str, str] = None
    ) -> str:
        # NOTE: Keep safe fallback for now (no production API calls)
        return f"Simulated response for: {query}"
    
    def _check_citation(self, domain: str, response: str) -> bool:
        clean_domain = domain.replace('https://', '').replace('http://', '').replace('www.', '').rstrip('/')
        return clean_domain.lower() in (response or "").lower()
    
    def _find_position(self, domain: str, response: str) -> Optional[int]:
        clean_domain = domain.replace('https://', '').replace('http://', '').replace('www.', '').rstrip('/')
        pos = (response or "").lower().find(clean_domain.lower())
        if pos == -1:
            return None
        
        response_length = len(response or "")
        if response_length == 0:
            return None
        
        position = min(10, max(1, int((pos / response_length) * 10) + 1))
        return position
    
    def _calculate_visibility_score(
        self,
        cited: bool,
        position: Optional[int],
        total_competitors: int,
        competitors_cited: int
    ) -> float:
        if not cited:
            return 0.0
        
        score = 50.0
        
        if position:
            score += (11 - position) * 3
        
        if total_competitors > 0:
            competitive_ratio = 1 - (competitors_cited / total_competitors)
            score += competitive_ratio * 20
        
        return min(100.0, score)
    
    def _save_citation_record(self, record: CitationRecord):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO citations 
            (timestamp, domain, query, engine, cited, position, competitors, response_snippet, visibility_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.timestamp,
            record.domain,
            record.query,
            record.engine,
            1 if record.cited else 0,
            record.position,
            json.dumps(record.competitor_cited),
            record.response_snippet,
            record.visibility_score
        ))
        
        conn.commit()
        conn.close()
    
    def get_visibility_stats(self, domain: str, days: int = 7) -> VisibilityStats:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        cursor.execute("""
            SELECT COUNT(DISTINCT query) 
            FROM citations 
            WHERE domain = ? AND timestamp >= ?
        """, (domain, start_date.isoformat()))
        total_queries = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM citations 
            WHERE domain = ? AND cited = 1 AND timestamp >= ?
        """, (domain, start_date.isoformat()))
        citations_won = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM citations 
            WHERE domain = ? AND cited = 0 AND timestamp >= ?
        """, (domain, start_date.isoformat()))
        citations_lost = cursor.fetchone()[0] or 0
        
        total_tests = citations_won + citations_lost
        citation_rate = (citations_won / total_tests * 100) if total_tests > 0 else 0
        
        cursor.execute("""
            SELECT AVG(position) 
            FROM citations 
            WHERE domain = ? AND cited = 1 AND position IS NOT NULL AND timestamp >= ?
        """, (domain, start_date.isoformat()))
        avg_position = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT AVG(visibility_score)
            FROM citations
            WHERE domain = ? AND timestamp >= ?
        """, (domain, start_date.isoformat()))
        visibility_score = cursor.fetchone()[0] or 0
        
        trend = self._calculate_trend(domain, days)
        conn.close()
        
        return VisibilityStats(
            total_queries=total_queries,
            citations_won=citations_won,
            citations_lost=citations_lost,
            citation_rate=citation_rate,
            avg_position=avg_position,
            top_winning_pages=[],
            top_losing_pages=[],
            competitor_wins={},
            visibility_score=visibility_score,
            trend=trend
        )
    
    def _calculate_trend(self, domain: str, days: int) -> str:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        end_date = datetime.now()
        mid_date = end_date - timedelta(days=days//2)
        start_date = end_date - timedelta(days=days)
        
        cursor.execute("""
            SELECT AVG(visibility_score)
            FROM citations
            WHERE domain = ? AND timestamp >= ?
        """, (domain, mid_date.isoformat()))
        recent_score = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT AVG(visibility_score)
            FROM citations
            WHERE domain = ? AND timestamp >= ? AND timestamp < ?
        """, (domain, start_date.isoformat(), mid_date.isoformat()))
        older_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        if recent_score > older_score * 1.1:
            return "improving"
        elif recent_score < older_score * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _get_tracked_queries(self, domain: str) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT query FROM tracked_queries 
            WHERE domain = ? AND active = 1
        """, (domain,))
        
        queries = [row[0] for row in cursor.fetchall()]
        conn.close()
        return queries
    
    def _get_competitors(self, domain: str) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT competitor_domain FROM competitors 
            WHERE domain = ?
        """, (domain,))
        
        competitors = [row[0] for row in cursor.fetchall()]
        conn.close()
        return competitors
    
    def get_historical_data(self, domain: str, days: int = 30) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        cursor.execute("""
            SELECT 
                DATE(timestamp) as date,
                AVG(visibility_score) as avg_score,
                SUM(CASE WHEN cited = 1 THEN 1 ELSE 0 END) as citations,
                COUNT(*) as total_tests
            FROM citations
            WHERE domain = ? AND timestamp >= ?
            GROUP BY DATE(timestamp)
            ORDER BY date ASC
        """, (domain, start_date.isoformat()))
        
        data = {
            'dates': [],
            'visibility_scores': [],
            'citations': [],
            'citation_rates': []
        }
        
        for row in cursor.fetchall():
            data['dates'].append(row[0])
            data['visibility_scores'].append(row[1] or 0)
            data['citations'].append(row[2])
            citation_rate = (row[2] / row[3] * 100) if row[3] > 0 else 0
            data['citation_rates'].append(citation_rate)
        
        conn.close()
        return data


if __name__ == "__main__":
    async def main():
        tracker = AISERPTracker()
        
        domain = "geon.vision"
        queries = [
            "What is generative engine optimization?",
            "Best GEO tools",
            "How to optimize for AI search",
            "GEO vs SEO differences"
        ]
        competitors = [
            "tripledart.com",
            "gofishdigital.com"
        ]
        
        tracker.add_tracked_queries(domain, queries)
        tracker.add_competitors(domain, competitors)
        
        print("Running tracking cycle...")
        results = await tracker.run_tracking_cycle(domain)
        print(f"✅ Tested {results['queries_tested']} queries")
        print(f"✅ Won {results['citations_won']} citations")
        print(f"✅ Lost {results['citations_lost']} citations")
        
        stats = tracker.get_visibility_stats(domain, days=7)
        print(f"\n📊 Visibility Score: {stats.visibility_score:.1f}/100")
        print(f"📊 Citation Rate: {stats.citation_rate:.1f}%")
        print(f"📊 Trend: {stats.trend}")
    
    asyncio.run(main())
