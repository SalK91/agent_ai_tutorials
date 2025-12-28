from __future__ import annotations

import json
from dataclasses import dataclass

from utils.llm import LLM


@dataclass(frozen=True)
class ConditionResult:
    ok: bool
    reason: str


def llm_answer_check(llm: LLM, question: str, answer: str) -> ConditionResult:
    """Optional LLM-based judge.

    In live mode, this asks the model to output JSON with {ok, reason}.
    """

    system = "You are a strict grader. Judge if the answer addresses the question."
    prompt = (
        "Return JSON only with keys ok (boolean) and reason (string).\n\n"
        f"QUESTION: {question}\n\nANSWER: {answer}\n"
    )
    resp = llm.complete(prompt, system=system, temperature=0.0, max_output_tokens=200)
    text = resp.text.strip()

    # Minimal JSON parsing without extra deps.
    # If parsing fails, fall back to heuristic.

    obj = json.loads(text)
    ok = bool(obj.get("ok"))
    reason = str(obj.get("reason", ""))
    return ConditionResult(ok, reason or "")
