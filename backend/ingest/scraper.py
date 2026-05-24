import requests
from bs4 import BeautifulSoup

# These are real Android/iOS telemetry-related doc pages we'll ingest.
# You can add more URLs later — this is just a starting set.
DOC_SOURCES = [
    {
        "url": "https://developer.android.com/topic/performance/vitals/anr",
        "platform": "android",
        "topic": "ANR"
    },
    {
        "url": "https://developer.android.com/topic/performance/vitals",
        "platform": "android",
        "topic": "Android Vitals overview"
    },
    {
        "url": "https://developer.android.com/topic/performance/power/battery-historian",
        "platform": "android",
        "topic": "Battery Historian"
    },
    {
        "url": "https://developer.apple.com/documentation/metrickit",
        "platform": "ios",
        "topic": "MetricKit overview"
    },
    {
        "url": "https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-shipping-app",
        "platform": "ios",
        "topic": "Xcode performance analysis"
    },
]

def scrape_page(url: str) -> str:
    """
    Fetches a doc page and returns clean plain text.
    BeautifulSoup parses the HTML — we strip nav, headers,
    footers so only the actual content goes into our DB.
    """
    headers = {"User-Agent": "Mozilla/5.0"}  # Some sites block requests without this
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Throws if 404, 500 etc.
    except requests.RequestException as e:
        print(f"  ⚠️  Could not fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noise: nav bars, sidebars, footers, scripts, styles
    for tag in soup(["nav", "header", "footer", "script", "style", "aside"]):
        tag.decompose()

    # Get the main content — different doc sites use different tags
    main = (
        soup.find("main") or
        soup.find("article") or
        soup.find("div", {"class": "devsite-article-body"}) or  # Android docs
        soup.find("div", {"id": "contents"}) or                 # Apple docs
        soup.body
    )

    text = main.get_text(separator="\n", strip=True) if main else ""
    return text


def load_all_docs() -> list[dict]:
    """
    Loops through all sources, scrapes each one,
    returns a list of { text, platform, topic, url } dicts.
    """
    docs = []
    for source in DOC_SOURCES:
        print(f"Fetching: {source['topic']} ({source['platform']})...")
        text = scrape_page(source["url"])
        
        if text:
            docs.append({
                "text": text,
                "platform": source["platform"],
                "topic": source["topic"],
                "url": source["url"],
            })
            print(f"  ✓ Got {len(text)} characters")
        else:
            print(f"  ✗ Skipped (empty response)")

    return docs
