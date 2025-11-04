"""Crawler agent responsible for fetching page content."""
from __future__ import annotations

from typing import Optional

import requests
from requests import Response

from ..state import LeoState
from ..utils.html_utils import extract_visible_text


USER_AGENT = "LeoCoreBot/0.2 (+https://github.com/leo-labs/leo-core)"


def _fetch(url: str, timeout: int = 10) -> Optional[Response]:
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        response.raise_for_status()
        return response
    except Exception:
        return None


def run(state: LeoState) -> LeoState:
    """Fetch remote HTML and extract visible text."""
    response = _fetch(state.url)
    html = response.text if response is not None else None
    text = extract_visible_text(html) if html else None

    return state.model_copy(update={"html": html, "text": text})


__all__ = ["run"]
