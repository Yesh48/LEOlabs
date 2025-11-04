"""Structure agent computes markup-related metrics."""
from __future__ import annotations

from ..state import LeoState
from ..utils.html_utils import parse_html
from ..utils.metrics_utils import normalize_count


def run(state: LeoState) -> LeoState:
    """Evaluate structured markup and populate structure metric."""
    soup = parse_html(state.html or "")
    metrics = dict(state.metrics)

    meta_tags = soup.find_all("meta")
    schema_tags = soup.find_all(attrs={"itemtype": True})
    og_tags = [tag for tag in meta_tags if (tag.get("property") or "").startswith("og:")]

    meta_score = normalize_count(len(meta_tags), max_expected=20)
    schema_score = normalize_count(len(schema_tags), max_expected=10)
    og_score = normalize_count(len(og_tags), max_expected=10)

    structure_score = round((meta_score + schema_score + og_score) / 3.0, 4)
    metrics["structure"] = structure_score

    return state.copy(update={"metrics": metrics})


__all__ = ["run"]
