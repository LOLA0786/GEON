import requests
from urllib.parse import urlparse
from scrape import scrape_website, clean_body_content
import re
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()


API_KEY = "AIzaSyCnN8o53yxjiGRwpgXOajt8I5q1R5JD3rc"
SEARCH_ENGINE_ID = "8641817a4af17475c"
EXCLUDE_DOMAINS = [
    "youtube.com", "google.com", "support.google.com", "accounts.google.com",
    "maps.google.com", "webcache.googleusercontent.com", "policies.google.com",
    "facebook.com", "apps.apple.com"
]

api_key = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(api_key=api_key,model="gemini-1.5-flash", temperature=0.2)

def extract_body_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # Look for typical article tags
    selectors = ['article', 'main', 'section', 'div[class*="content"]', 'div[class*="main"]']
    for sel in selectors:
        section = soup.select_one(sel)
        if section:
            return section.get_text(separator=" ", strip=True)

    # Fallback to full body
    return soup.body.get_text(separator=" ", strip=True) if soup.body else ""

def extract_brand_mentions_with_context(text, brand_name, window=1):
    brand_name = brand_name.lower()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    relevant = []

    for i, s in enumerate(sentences):
        if brand_name in s.lower():
            start = max(0, i - window)
            end = min(len(sentences), i + window + 1)
            relevant.extend(sentences[start:end])
    
    return "\n".join(relevant)

def extract_domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return None

def get_top_10_unique_domain_urls(brand_name):
    print(f"Searching for brand: {brand_name}")
    unique_urls = []
    seen_domains = set()

    for start in [1, 11]:  # First two pages (start=1 and start=11)
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={brand_name}&start={start}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Error:", response.json())
            break

        results = response.json().get("items", [])
        for item in results:
            href = item.get("link")
            domain = extract_domain(href)
            if not domain or domain in seen_domains:
                continue
            if any(exclude in domain for exclude in EXCLUDE_DOMAINS):
                continue
            if brand_name.lower() not in href.lower():
                continue
            unique_urls.append(href)
            seen_domains.add(domain)

            if len(unique_urls) >= 10:
                break
        if len(unique_urls) >= 10:
            break

    print(f"Top {len(unique_urls)} unique-domain URLs found for '{brand_name}':")
    for url in unique_urls:
        print(" -", url)

    return unique_urls



def analyze_sentiment_on_the_fly(brand_name):
    urls = get_top_10_unique_domain_urls(brand_name)
    results = []

    for url in urls:
        try:
            html = scrape_website(url)
            body = extract_body_content(html)
            cleaned = clean_body_content(body)

            if not cleaned.strip():
                continue  # Skip empty cleaned content

            # Construct prompt for Gemini
            prompt = f"""
            You are a sentiment analysis engine. Analyze the sentiment of the following mention about the brand '{brand_name}'.

            Mention:
            \"\"\"{cleaned}\"\"\"

            Return one of these labels: Positive, Negative, Neutral. Also include a short reason.
            Format: {{ "sentiment": "Label", "reason": "Explanation" }}
            """

            response = model.invoke(prompt)
            sentiment_analysis = response.content.strip()
            
            data = {
                "url": url,
                "analysis": sentiment_analysis
            }
            print(data)
            results.append(data)

        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            continue

    return results

def get_brand_web_mentions_and_texts(brand_name):
    results = []
    urls = get_top_10_unique_domain_urls(brand_name)

    for url in urls:
        try:
            html = scrape_website(url)
            body = extract_body_content(html)
            cleaned = clean_body_content(body)

            # mentions = extract_brand_mentions_with_context(cleaned, brand_name, window=1)
            mentions = cleaned

            if mentions.strip():  # Skip empty mentions
                results.append({
                    "url": url,
                    "mentions": mentions.strip()
                    # "mentions": f"data scraped from {url}"
                })
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            continue

    return results
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(api_key)
model = ChatGoogleGenerativeAI(api_key=api_key,model="gemini-1.5-flash", temperature=0.2)

def analyze_sentiment_with_gemini(brand_name):
    mentions_data = get_brand_web_mentions_and_texts(brand_name)

    if not mentions_data:
        print("⚠️ No mentions found.")
        return []

    results = []
    for entry in mentions_data:
        url = entry["url"]
        mention_text = entry["mentions"]

        prompt = f"""
        You are a sentiment analysis engine. Analyze the sentiment of the following mention about the brand '{brand_name}'.

        Mention:
        \"\"\"{mention_text}\"\"\"

        Return one of these labels: Positive, Negative, Neutral. Also include a short reason.
        Format: {{ "sentiment": "Label", "reason": "Explanation" }}
        """

        try:
            response = model.invoke(prompt)
            sentiment_analysis = response.content.strip()

            results.append({
                "url": url,
                # "mention": mention_text,
                "analysis": sentiment_analysis
            })

        except Exception as e:
            print(f"❌ Error analyzing sentiment for {url}: {e}")
            continue

    return results


if __name__ == "__main__":
    brand = "Lambdatest"
    analysis_results = analyze_sentiment_on_the_fly(brand)

    for idx, item in enumerate(analysis_results, 1):
        print(f"\n[{idx}] 🔗 {item['url']}")
        # print(f"--- Mention ---\n{item['mention']}")
        print(f"--- Sentiment Analysis ---\n{item['analysis']}")

    # competitors = get_competitors(brand)
    # print("Competitors:", competitors)

