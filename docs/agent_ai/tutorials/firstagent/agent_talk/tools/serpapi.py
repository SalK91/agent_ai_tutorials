from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import requests


@dataclass(frozen=True)
class WebResult:
    title: str
    link: str
    snippet: str | None = None


class SerpAPIError(RuntimeError):
    pass


def search_web(query: str, api_key: str, num_results: int = 5, timeout: int = 20) -> List[WebResult]:
    """Search the web using SerpAPI (Google) and return top organic results."""
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
    }
    r = requests.get(url, params=params, timeout=timeout)
    if r.status_code != 200:
        raise SerpAPIError(f"SerpAPI request failed: HTTP {r.status_code} {r.text[:200]}")
    data = r.json()
    organic = data.get("organic_results", []) or []
    out: List[WebResult] = []
    for item in organic[:num_results]:
        out.append(
            WebResult(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet"),
            )
        )
    return out
