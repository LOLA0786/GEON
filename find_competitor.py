import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Set
import time

class EnhancedCompetitorFinder:
    def __init__(self, google_api_key=None, search_engine_id=None, ai_model=None):
        """
        Initialize with Google Custom Search API credentials and AI model
        
        Args:
            google_api_key: Google Custom Search API key
            search_engine_id: Google Custom Search Engine ID
            ai_model: AI model instance (e.g., Gemini, OpenAI, etc.)
        """
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.ai_model = ai_model
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_website(self, url: str) -> str:
        """Scrape website content"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return ""
    
    def extract_body_content(self, html: str) -> str:
        """Extract main body content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text from body or main content
        body = soup.find('body') or soup
        return body.get_text()
    
    def clean_body_content(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()[:5000]  # Limit to 5000 chars to avoid token limits
    
    def discover_relevant_pages(self, website_url: str, max_pages: int = 5) -> List[str]:
        """Find internal pages likely to describe the company"""
        try:
            html = self.scrape_website(website_url)
            soup = BeautifulSoup(html, "html.parser")
            
            domain = urlparse(website_url).netloc
            relevant_keywords = [
                "about", "solution", "service", "product", "platform", 
                "industry", "who-we-are", "company", "what-we-do"
            ]
            
            found_urls = set([website_url])  # Always include homepage
            
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                full_url = urljoin(website_url, href)
                
                # Keep only same-domain internal links
                if urlparse(full_url).netloc != domain:
                    continue
                
                # Keep relevant pages only
                if any(kw in full_url.lower() for kw in relevant_keywords):
                    found_urls.add(full_url)
                    
                if len(found_urls) >= max_pages:
                    break
            
            return list(found_urls)[:max_pages]
        except Exception as e:
            print(f"❌ Error discovering pages: {e}")
            return [website_url]
    
    def fetch_from_google(self, query: str) -> str:
        """Fetch search results from Google Custom Search API"""
        if not self.google_api_key or not self.search_engine_id:
            print("⚠️ Google API credentials not provided")
            return ""
        
        try:
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': 10
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"❌ Google API Error: {response.json()}")
                return ""
            
            items = response.json().get("items", [])
            return "\n".join([
                f"{item.get('title', '')} {item.get('snippet', '')}"
                for item in items
            ])
        except Exception as e:
            print(f"❌ Google fetch error: {e}")
            return ""
    
    def fetch_from_ai(self, prompt: str) -> List[str]:
        """Get competitor list from AI model"""
        if not self.ai_model:
            print("⚠️ AI model not provided")
            return []
        
        try:
            response = self.ai_model.invoke(prompt)
            content = response.content.strip()
            
            # Try to extract JSON list
            json_match = re.search(r'\[.*?\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback: extract quoted strings
            return re.findall(r'"([^"]+)"', content)
            
        except Exception as e:
            print(f"❌ AI error: {e}")
            return []
    
    def detect_industry_from_website(self, website_url: str) -> str:
        """Detect industry/domain from website content"""
        pages_to_scrape = self.discover_relevant_pages(website_url, max_pages=3)
        
        all_text = ""
        for page in pages_to_scrape:
            try:
                html = self.scrape_website(page)
                body_html = self.extract_body_content(html)
                cleaned_text = self.clean_body_content(body_html)
                if cleaned_text:
                    all_text += f"\n{cleaned_text}"
            except Exception as e:
                print(f"⚠️ Could not scrape {page}: {e}")
        
        if not all_text.strip():
            return "Unknown"
        
        # Use AI to detect industry
        if self.ai_model:
            domain_prompt = f"""
            Analyze the following website content and determine the exact industry/domain.
            Return only the industry name (e.g., "E-commerce", "SaaS", "Fintech", "Healthcare"):
            
            {all_text[:3000]}
            """
            try:
                response = self.ai_model.invoke(domain_prompt)
                return response.content.strip()
            except:
                pass
        
        # Fallback: keyword-based detection
        return self.detect_industry_keywords(all_text)
    
    def detect_industry_keywords(self, content: str) -> str:
        """Fallback industry detection using keywords"""
        content_lower = content.lower()
        
        industry_patterns = {
            'E-commerce': ['shop', 'store', 'buy', 'cart', 'checkout', 'product', 'retail'],
            'SaaS': ['software', 'platform', 'dashboard', 'api', 'cloud', 'subscription'],
            'Fintech': ['payment', 'finance', 'banking', 'investment', 'money', 'wallet'],
            'Healthcare': ['health', 'medical', 'doctor', 'patient', 'treatment', 'clinic'],
            'Education': ['learn', 'course', 'student', 'education', 'training', 'school'],
            'Travel': ['hotel', 'flight', 'travel', 'booking', 'vacation', 'trip'],
            'Food & Beverage': ['restaurant', 'food', 'delivery', 'menu', 'order', 'cuisine'],
            'Real Estate': ['property', 'real estate', 'home', 'rent', 'house', 'apartment'],
            'Marketing': ['marketing', 'advertising', 'campaign', 'brand', 'promotion'],
            'Logistics': ['shipping', 'delivery', 'logistics', 'transport', 'supply chain']
        }
        
        best_match = "Unknown"
        max_matches = 0
        
        for industry, keywords in industry_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            if matches > max_matches:
                max_matches = matches
                best_match = industry
        
        return best_match if max_matches >= 2 else "Unknown"

def find_competitors_advanced(
    website_url: str = None,
    brand_name: str = None, 
    google_api_key: str = None,
    search_engine_id: str = None,
    ai_model = None,
    include_india: bool = True,
    include_global: bool = True
) -> Dict:
    """
    Advanced competitor finder using AI and Google Search
    
    Args:
        website_url: Company website URL (optional)
        brand_name: Brand name to search for
        google_api_key: Google Custom Search API key
        search_engine_id: Google Custom Search Engine ID  
        ai_model: AI model instance (Gemini, OpenAI, etc.)
        include_india: Whether to search for India-specific competitors
        include_global: Whether to search for global competitors
    
    Returns:
        Dict with competitor analysis results
    """
    
    finder = EnhancedCompetitorFinder(google_api_key, search_engine_id, ai_model)
    
    # Initialize results
    result = {
        "brand_name": brand_name,
        "website_url": website_url,
        "domain": "Unknown",
        "india_competitors": [],
        "global_competitors": [],
        "search_queries_used": [],
        "analysis_method": []
    }
    
    # Detect industry from website if provided
    if website_url:
        print(f"🔍 Analyzing website: {website_url}")
        result["domain"] = finder.detect_industry_from_website(website_url)
        result["analysis_method"].append("website_analysis")
        print(f"📊 Detected industry: {result['domain']}")
    
    # If no brand name provided, try to extract from website
    if not brand_name and website_url:
        try:
            domain = urlparse(website_url).netloc
            brand_name = domain.replace('www.', '').split('.')[0].title()
            result["brand_name"] = brand_name
        except:
            print("❌ Could not determine brand name")
            return result
    
    if not brand_name:
        print("❌ Brand name is required")
        return result
    
    print(f"🎯 Finding competitors for: {brand_name}")
    
    india_competitors = set()
    global_competitors = set()
    
    # Method 1: Direct AI knowledge
    if ai_model:
        result["analysis_method"].append("ai_knowledge")
        
        if include_india:
            print("🇮🇳 Getting India competitors from AI...")
            india_prompt = f"""
            List the top competitors of '{brand_name}' in India. 
            Focus on companies active in the last 3 years in the {result['domain']} industry.
            Return only a JSON list of company names: ["Company1", "Company2", ...]
            """
            india_competitors.update(finder.fetch_from_ai(india_prompt))
        
        if include_global:
            print("🌍 Getting global competitors from AI...")
            global_prompt = f"""
            List the top global competitors of '{brand_name}'. 
            Focus on companies active in the last 3 years in the {result['domain']} industry.
            Return only a JSON list of company names: ["Company1", "Company2", ...]
            """
            global_competitors.update(finder.fetch_from_ai(global_prompt))
    
    # Method 2: Google Search + AI Analysis
    if google_api_key and search_engine_id and ai_model:
        result["analysis_method"].append("google_search")
        
        if include_india:
            print("🔍 Searching Google for India competitors...")
            india_queries = [
                f"{brand_name} competitors in India",
                f"{brand_name} alternatives India",
                f"top {result['domain']} companies India vs {brand_name}"
            ]
            
            for query in india_queries:
                snippets = finder.fetch_from_google(query)
                if snippets:
                    result["search_queries_used"].append(query)
                    extract_prompt = f"""
                    From the following search results, extract only competitor company names 
                    for '{brand_name}' in India in the {result['domain']} industry.
                    Return only a JSON list: ["Company1", "Company2", ...]
                    
                    Search Results:
                    {snippets}
                    """
                    india_competitors.update(finder.fetch_from_ai(extract_prompt))
                time.sleep(1)  # Rate limiting
        
        if include_global:
            print("🔍 Searching Google for global competitors...")
            global_queries = [
                f"{brand_name} competitors worldwide",
                f"{brand_name} vs alternatives global",
                f"top {result['domain']} companies globally like {brand_name}"
            ]
            
            for query in global_queries:
                snippets = finder.fetch_from_google(query)
                if snippets:
                    result["search_queries_used"].append(query)
                    extract_prompt = f"""
                    From the following search results, extract only competitor company names 
                    for '{brand_name}' globally in the {result['domain']} industry.
                    Return only a JSON list: ["Company1", "Company2", ...]
                    
                    Search Results:
                    {snippets}
                    """
                    global_competitors.update(finder.fetch_from_ai(extract_prompt))
                time.sleep(1)  # Rate limiting
    
    # Clean and sort results
    result["india_competitors"] = sorted([comp for comp in india_competitors if comp and len(comp) > 1])
    result["global_competitors"] = sorted([comp for comp in global_competitors if comp and len(comp) > 1])
    
    print(f"✅ Found {len(result['india_competitors'])} India competitors")
    print(f"✅ Found {len(result['global_competitors'])} global competitors")
    
    return result

# Real implementation functions
def setup_openai_model(api_key: str):
    """Setup OpenAI model as alternative to Gemini"""
    try:
        import openai
        
        class OpenAIModel:
            def __init__(self, api_key):
                openai.api_key = api_key
                
            def invoke(self, prompt):
                class Response:
                    def __init__(self, content):
                        self.content = content
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500,
                        temperature=0.3
                    )
                    return Response(response.choices[0].message.content)
                except Exception as e:
                    print(f"OpenAI API error: {e}")
                    return Response("[]")
        
        return OpenAIModel(api_key)
    except ImportError:
        print("OpenAI library not installed. Install with: pip install openai")
        return None

from langchain_google_genai import ChatGoogleGenerativeAI

def setup_langchain_gemini(api_key: str):
    """
    Setup Gemini Pro via LangChain ChatGoogleGenerativeAI
    """
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # or gemini-1.5-pro
            google_api_key=api_key,
            temperature=0.2,
            max_output_tokens=512
        )

        class LangChainGeminiWrapper:
            def __init__(self, model):
                self.model = model
            
            def invoke(self, prompt: str):
                class Response:
                    def __init__(self, content):
                        self.content = content
                try:
                    result = self.model.invoke(prompt)
                    # result is a AIMessage from LangChain, extract content
                    return Response(result.content if hasattr(result, "content") else str(result))
                except Exception as e:
                    print(f"LangChain Gemini API error: {e}")
                    return Response("[]")

        return LangChainGeminiWrapper(model)
    except ImportError:
        print("LangChain Google GenAI not installed. Install with: pip install langchain-google-genai")
        return None

def find_competitors_without_ai(
    website_url: str = None,
    brand_name: str = None,
    google_api_key: str = None,
    search_engine_id: str = None
) -> Dict:
    """
    Simplified version that works without AI - uses Google Search + keyword extraction
    """
    finder = EnhancedCompetitorFinder(google_api_key, search_engine_id, None)
    
    result = {
        "brand_name": brand_name,
        "website_url": website_url,
        "domain": "Unknown",
        "india_competitors": [],
        "global_competitors": [],
        "search_queries_used": [],
        "analysis_method": []
    }
    
    # Get brand name from website if not provided
    if not brand_name and website_url:
        try:
            domain = urlparse(website_url).netloc
            brand_name = domain.replace('www.', '').split('.')[0].title()
            result["brand_name"] = brand_name
        except:
            print("❌ Could not determine brand name")
            return result
    
    if not brand_name:
        print("❌ Brand name is required")
        return result
    
    # Detect industry from website
    if website_url:
        result["domain"] = finder.detect_industry_keywords("")  # Use fallback method
        result["analysis_method"].append("website_analysis")
    
    # Search Google and extract competitors using keyword matching
    if google_api_key and search_engine_id:
        result["analysis_method"].append("google_search")
        
        # India competitors
        india_queries = [
            f"{brand_name} competitors India",
            f"{brand_name} vs alternatives India",
            f"top companies like {brand_name} India"
        ]
        
        india_competitors = set()
        for query in india_queries:
            snippets = finder.fetch_from_google(query)
            if snippets:
                result["search_queries_used"].append(query)
                # Extract potential competitor names using regex
                competitors = extract_competitors_from_text(snippets, brand_name)
                india_competitors.update(competitors)
            time.sleep(1)
        
        # Global competitors
        global_queries = [
            f"{brand_name} competitors",
            f"{brand_name} alternatives",
            f"companies similar to {brand_name}"
        ]
        
        global_competitors = set()
        for query in global_queries:
            snippets = finder.fetch_from_google(query)
            if snippets:
                result["search_queries_used"].append(query)
                competitors = extract_competitors_from_text(snippets, brand_name)
                global_competitors.update(competitors)
            time.sleep(1)
        
        result["india_competitors"] = sorted(list(india_competitors))
        result["global_competitors"] = sorted(list(global_competitors))
    
    return result

def extract_competitors_from_text(text: str, brand_name: str) -> Set[str]:
    """Extract competitor names from search result text using patterns"""
    competitors = set()
    
    # Common patterns in search results
    patterns = [
        r'(?:vs|versus|compared to|alternative to|competitor to|like|similar to)\s+([A-Z][a-zA-Z0-9\s]{2,20})',
        r'([A-Z][a-zA-Z0-9\s]{2,20})\s+(?:vs|versus|compared to|competitor|alternative)',
        r'(?:top|best|leading)\s+(?:companies|platforms|services|tools)?\s*:?\s*([A-Z][a-zA-Z0-9\s,]{10,100})',
        r'(?:including|such as|like)\s+([A-Z][a-zA-Z0-9\s,]{10,100})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Split on commas and clean
            names = [name.strip() for name in match.split(',')]
            for name in names:
                name = re.sub(r'[^\w\s]', '', name).strip()
                if (len(name) > 2 and len(name) < 30 and 
                    name.lower() != brand_name.lower() and
                    not any(word in name.lower() for word in ['the', 'and', 'best', 'top', 'leading'])):
                    competitors.add(name.title())
    
    return competitors

# Example usage
if __name__ == "__main__":
    api_key = "AIzaSyCnN8o53yxjiGRwpgXOajt8I5q1R5JD3rc"
    engine_id = "8641817a4af17475c"
    model = setup_langchain_gemini(api_key)  # now using LangChain

    result = find_competitors_advanced(
        website_url="https://www.lambdatest.com/",
        brand_name="lambdatest",
        google_api_key=api_key,
        search_engine_id=engine_id,
        ai_model=model,
        include_india=True,
        include_global=True
    )
    print(result)
