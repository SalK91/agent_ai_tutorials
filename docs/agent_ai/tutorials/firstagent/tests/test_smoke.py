from __future__ import annotations

from agent_talk.config import Settings
from agent_talk.llm import LLM
from agent_talk.condition import heuristic_answer_check
from agent_talk.memory import JsonMemory
from agent_talk.planner import make_plan
from agent_talk.agent import run_agent


def test_mock_llm_runs():
    settings = Settings(openai_api_key=None, openai_model="gpt-4.1-mini", serpapi_api_key=None)
    llm = LLM(settings)
    r = llm.complete("Hello")
    assert r.used_mock
    assert "mock" in r.text.lower()


def test_condition_basic():
    long_answer = (
        "Agentic systems loop over thinking and acting. "
        "They decompose goals into steps, check progress, and iterate until done. "
        "This answer is intentionally long enough to pass a simple heuristic."
    )
    res = heuristic_answer_check("What is agentic AI?", long_answer)
    assert res.ok


def test_memory_read_write(tmp_path):
    m = JsonMemory(tmp_path / "mem.json")
    m.write("a", 123)
    assert m.read("a") == 123


def test_plan_parse(tmp_path):
    settings = Settings(openai_api_key=None, openai_model="gpt-4.1-mini", serpapi_api_key=None)
    llm = LLM(settings)
    plan = make_plan(llm, "Do a thing")
    assert plan.todos


def test_agent_mock(tmp_path):
    settings = Settings(openai_api_key=None, openai_model="gpt-4.1-mini", serpapi_api_key=None)
    llm = LLM(settings)
    mem = JsonMemory(tmp_path / "memory.json")
    res = run_agent(llm=llm, goal="Explain the ReAct agent pattern", memory=mem, allow_web=False, max_iters=3)
    assert res.answer
