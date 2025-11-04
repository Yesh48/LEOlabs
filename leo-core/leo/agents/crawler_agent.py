"""
leo/agents/crawler_agent.py
Fetches a website’s HTML and extracts visible text content.
This is the entry point of the LEO Core audit pipeline.
"""

import requests
from bs4 import BeautifulSoup
from leo.state import LeoState


class CrawlerAgent:
    """Fetch and parse the target website."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def run(self, state: LeoState) -> LeoState:
        """Fetch HTML and extract readable text."""
        url = state.url
        print(f"[CrawlerAgent] Fetching {url} ...")

        try:
            response = requests.get(url, timeout=self.timeout, headers={"User-Agent": "LEO-Core/0.2"})
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"[CrawlerAgent] ❌ Failed to fetch {url}: {e}")
            state.html = ""
            state.text = ""
            return state

        # Store HTML
        state.html = html

        # Parse and extract text
        soup = BeautifulSoup(html, "html.parser")

        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        visible_text = " ".join(soup.stripped_strings)
        state.text = visible_text[:100000]  # cap to avoid large pages

        print(f"[CrawlerAgent] ✅ Extracted {len(visible_text.split())} words of text")
        return state
