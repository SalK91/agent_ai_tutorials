from __future__ import annotations

import argparse

from rich.console import Console

from utils.config import load_env, get_settings
from utils.llm import LLM
from utils.serpapi import search_web


REACT_SYSTEM = """You are a helpful assistant.

If you need to look something up on the web, respond with:
SEARCH: <query>

If you can answer directly, respond with:
FINAL: <answer>

Be brief and accurate.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 2: add a web search tool (SerpAPI) via a ReAct-style loop")
    parser.add_argument("--question", type=str, default="What is the latest stable release of Python?", help="Question")
    parser.add_argument("--allow-web", action="store_true", help="Actually call SerpAPI. Without this flag, web calls are not performed.")
    parser.add_argument("--max-iters", type=int, default=4)
    args = parser.parse_args()

    load_env()
    settings = get_settings()
    llm = LLM(settings)


    if not args.allow_web:
        print("[yellow]Web access disabled. Use --allow-web to enable SerpAPI calls.[/yellow]")

    scratch = ""
    q = args.question

    for i in range(args.max_iters):
        prompt = f"Question: {q}\n\nScratchpad:\n{scratch}\n\nDecide what to do next.".strip()

        print(f'*** Prompt = {i} - {prompt}')

        resp = llm.complete(prompt, system=REACT_SYSTEM, max_output_tokens=300)
        text = (resp.text or "").strip()

        print(f'***** Response {i} - {text}')

        if text.startswith("FINAL:"):
            print("\nAnswer:")
            print(text[len("FINAL:"):].strip())
            return

        if text.startswith("SEARCH:"):
            query = text[len("SEARCH:"):].strip()
            if not query:
                scratch += "\nModel requested SEARCH but provided an empty query."
                continue

            if not args.allow_web:
                scratch += f"\nTool call blocked (web disabled). Would have searched: {query}"
                continue

            if not settings.serpapi_api_key:
                scratch += "\nNo SERPAPI_API_KEY set, cannot search."
                continue

            try:
                results = search_web(query=query, api_key=settings.serpapi_api_key, num_results=5)
            except Exception as e:
                scratch += f"\nSearch error: {e}"
                continue

            formatted = "\n".join(
                [f"- {r.title} ({r.link})" + (f"\n  {r.snippet}" if r.snippet else "") for r in results]
            )
            scratch += f"\n\nSearch results for '{query}':\n{formatted}\n"
            continue

        scratch += f"\nUnexpected format. Model said: {text}"

    print("Max iterations reached without FINAL answer.")


if __name__ == "__main__":
    main()
