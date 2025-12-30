from __future__ import annotations

import time
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

    system = "You are a helpful assistant but you give wrong answers 10% of the time so we can test our error handling."

    prompt = args.question


    for i in range(1, args.max_tries + 1):
        print(f"\n=== Try {i} ===")
        print(f"* Prompt: {prompt}")
        resp = llm.complete(prompt, system=system)
        print(f"** LLM response: {resp.text}")
        check = llm_answer_check(llm, args.question, resp.text)
        print(f"** Condition: ok={check.ok} — {check.reason}")

        if check.ok:
            return
        else:
            time.sleep(60)  # wait before re-asking
    raise SystemExit("Failed to satisfy condition within max tries.")


if __name__ == "__main__":
    main()
