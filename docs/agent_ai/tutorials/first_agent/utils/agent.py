from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from rich.console import Console

from utils.llm import LLM
from utils.planner import make_plan
from utils.memory import JsonMemory
from utils.serpapi import search_web
from utils.condition import llm_answer_check

import time

@dataclass
class AgentResult:
    answer: str
    used_web: bool
    steps: List[str]


def run_agent(
    llm: LLM,
    goal: str,
    memory: JsonMemory,
    allow_web: bool = False,
    serpapi_api_key: str | None = None,
    max_iters: int = 6,
) -> AgentResult:
    """A tiny agent loop.

    Algorithm (intentionally simple):
    - build a plan (todo list)
    - for each iteration: ask LLM for next action
      - if it outputs a SEARCH: query and web is allowed, call SerpAPI and stash notes
      - otherwise treat as draft answer
    - stop when heuristic check passes

    The point is to demonstrate the agent pattern, not to be production-grade.
    """

    steps: List[str] = []
    used_web = False

    plan = make_plan(llm, goal)
    print(f"*** Agent plan: {plan.todos}")
    print('\n \n')
    memory.write("goal", goal)
    memory.write("plan", plan.todos)

    notes_key = "notes"
    memory.write(notes_key, [])

    system = (
        "You are a helpful agent."
        "You may optionally ask to SEARCH if you need external facts."
        "If you want to search, output exactly: SEARCH: <your query>."
        "Otherwise output your answer directly."
    )

    last_answer = ""
    for i in range(1, max_iters + 1):
        notes = memory.read(notes_key) or []
        prompt = (
            f"GOAL: {goal}\n"
            f"PLAN: {plan.todos}\n"
            f"NOTES: {notes}\n\n"
            "What should you do next? If you need web facts, use SEARCH:. Otherwise answer the goal."
        )

        time.sleep(60)  # to avoid rate limits in demos
        resp = llm.complete(prompt, system=system, max_output_tokens=512)
        text = (resp.text or "").strip()
        print(f'*** Iter {i} response: {text}')
        steps.append(f"iter {i}: {text[:200]}")

        if allow_web and text.upper().startswith("SEARCH:"):
            if not serpapi_api_key:
                steps.append("web search requested but SERPAPI_API_KEY not set; skipping")
                continue
            query = text.split(":", 1)[1].strip()
            try:
                results = search_web(query=query, api_key=serpapi_api_key, num_results=5)
            except Exception as e:
                steps.append(f"web search failed: {e}")
                continue
            used_web = True
            # store a compact note
            compact = [
                {"title": r.title, "link": r.link, "snippet": r.snippet}
                for r in results
            ]
            notes.append({"query": query, "results": compact})
            memory.write(notes_key, notes)
            continue

        # otherwise treat as candidate answer
        if text.upper().startswith("FINAL:"):
            last_answer = text.split(":", 1)[1].strip()
        else:
            last_answer = text
        check = llm_answer_check(llm, goal, last_answer)
        steps.append(f"check: ok={check.ok} reason={check.reason}")
        if check.ok:
            break

    memory.write("final_answer", last_answer)
    return AgentResult(answer=last_answer, used_web=used_web, steps=steps)
