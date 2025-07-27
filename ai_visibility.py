import requests
from urllib.parse import urlparse
from scrape import scrape_website, extract_body_content, clean_body_content

API_KEY = "AIzaSyCnN8o53yxjiGRwpgXOajt8I5q1R5JD3rc"
SEARCH_ENGINE_ID = "8641817a4af17475c"
EXCLUDE_DOMAINS = [
    "youtube.com", "google.com", "support.google.com", "accounts.google.com",
    "maps.google.com", "webcache.googleusercontent.com", "policies.google.com",
    "facebook.com"
]

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

def get_brand_web_mentions_and_texts(brand_name):
    results = []
    urls = get_top_10_unique_domain_urls(brand_name)

    for url in urls:
        try:
            html = scrape_website(url)
            body = extract_body_content(html)
            cleaned = clean_body_content(body)

            results.append({
                "url": url,
                "content": cleaned  # Preview only first 1000 chars
            })

        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            continue

    return results

if __name__ == "__main__":
    brand = "Veefin"
    data = get_brand_web_mentions_and_texts(brand)

    for idx, item in enumerate(data, 1):
        print(f"\n[{idx}] 🔗 {item['url']}\n--- Content Preview ---\n{item['content']}\n")
