from __future__ import annotations

import argparse
from utils.config import load_env, get_settings
from utils.llm import LLM
from utils.condition import llm_answer_check

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 1: add a simple condition to verify the answer")
    parser.add_argument("--question", type=str, default="Explain ReAct in 3 bullets", help="Prompt/question to ask")
    parser.add_argument("--max-tries", type=int, default=3, help="Max re-ask attempts")
    args = parser.parse_args()

    load_env()
    settings = get_settings()
    llm = LLM(settings)

    system = "You are a helpful assistant. Be concise and follow the requested format."

    prompt = args.question


    for i in range(1, args.max_tries + 1):
        print(f"\n=== Try {i} ===")
        print(f"[dim]Prompt: {prompt}[/dim]")
        resp = llm.complete(prompt, system=system)
        print(f"[dim]LLM response: {resp.text}[/dim]")
        check = llm_answer_check(args.question, resp.text)
        print(f"[dim]Condition: ok={check.ok} — {check.reason}[/dim]")

        if check.ok:
            return

        # Minimal "self-correction" prompt
        prompt = (
            f"The previous answer did not satisfy the requirement ({check.reason}).\n"
            f"Please answer the question again and strictly follow the requested format.\n\n"
            f"Question: {args.question}"
        )

    raise SystemExit("Failed to satisfy condition within max tries.")


if __name__ == "__main__":
    main()
