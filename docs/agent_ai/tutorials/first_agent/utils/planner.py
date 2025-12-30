from __future__ import annotations

from dataclasses import dataclass
from typing import List
import re

from utils.llm import LLM


@dataclass
class Plan:
    goal: str
    todos: List[str]


def parse_bullets(text: str) -> List[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    bullets: List[str] = []
    for l in lines:
        m = re.match(r"^(?:-|•|\d+[.)])\s+(.*)$", l)
        if m:
            bullets.append(m.group(1).strip())
    if bullets:
        return bullets
    # fallback: treat each non-empty line as an item
    return lines


def make_plan(llm: LLM, goal: str, max_todos: int = 6) -> Plan:
    prompt = (
        "Write a TODO list to achieve the user's goal.\n"
        "Rules:\n"
        f"- Maximum {max_todos} bullet items\n"
        "- Make each item actionable\n\n"
        f"GOAL: {goal}"
    )
    resp = llm.complete(prompt, system="You are a careful planner.")
    todos = parse_bullets(resp.text)[:max_todos]
    return Plan(goal=goal, todos=todos)
