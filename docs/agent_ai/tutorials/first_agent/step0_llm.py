from __future__ import annotations
import argparse
from utils.config import load_env, get_settings
from utils.llm import LLM


def main() -> None:

    parser = argparse.ArgumentParser(description="Step 0: a single LLM call")
    parser.add_argument("--question", type=str, default="What is agentic AI? (give brief response)", help="Prompt/question to ask")
    args = parser.parse_args()
    
    print(f'**Load env')
    
    load_env()
    print(f'**Get llm settings')
    
    settings = get_settings()
    llm = LLM(settings)

    print(f'**Call llm')
    resp = llm.complete(args.question, system="You are a helpful assistant.")

    print(f"Model: {resp.model} (mock={resp.used_mock})")
    print(resp.text)


if __name__ == "__main__":
    main()
