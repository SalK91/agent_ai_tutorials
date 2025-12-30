from __future__ import annotations

import argparse

from rich.console import Console

from utils.config import load_env, get_settings
from utils.llm import LLM
from utils.memory import JsonMemory
from utils.agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 3: a minimal agent loop (plan + memory + tools)")
    parser.add_argument("--goal", type=str, default="Find two reputable sources explaining the ReAct agent pattern and summarize them.")
    parser.add_argument("--allow-web", action="store_true", help="Allow using SerpAPI (requires SERPAPI_API_KEY)")
    parser.add_argument("--max-iters", type=int, default=5)
    parser.add_argument("--memory-path", type=str, default="./memory.json", help="JSON file for long-term memory")
    args = parser.parse_args()

    load_env()
    settings = get_settings()
    llm = LLM(settings)
    memory = JsonMemory(args.memory_path)

    result = run_agent(
        goal=args.goal,
        llm=llm,
        memory=memory,
        allow_web=args.allow_web,
        serpapi_api_key=settings.serpapi_api_key,
        max_iters=args.max_iters,
    )

    console = Console()
    console.rule("Final")
    console.print(result.answer)


if __name__ == "__main__":
    main()
