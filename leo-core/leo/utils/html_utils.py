"""HTML utility helpers for Leo Core."""
from __future__ import annotations

from bs4 import BeautifulSoup


def extract_visible_text(html: str) -> str:
    """Return a cleaned string containing visible text from HTML."""
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


def parse_html(html: str) -> BeautifulSoup:
    """Parse HTML into a BeautifulSoup document."""
    return BeautifulSoup(html or "", "html.parser")


__all__ = ["extract_visible_text", "parse_html"]
