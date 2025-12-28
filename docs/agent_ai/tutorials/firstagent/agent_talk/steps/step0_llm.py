from __future__ import annotations

import argparse

from rich.console import Console

from ..config import load_env, get_settings
from ..llm import LLM


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 0: a single LLM call")
    parser.add_argument("--question", type=str, default="What is agentic AI?", help="Prompt/question to ask")
    args = parser.parse_args()

    load_env()
    settings = get_settings()
    llm = LLM(settings)

    resp = llm.complete(args.question, system="You are a helpful assistant.")

    c = Console()
    c.print(f"[bold]Model[/bold]: {resp.model}  [dim](mock={resp.used_mock})[/dim]")
    c.print(resp.text)


if __name__ == "__main__":
    main()
