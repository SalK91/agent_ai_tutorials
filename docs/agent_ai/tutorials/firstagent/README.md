# Agent Talk 2025 (Python port)

This repository contains a Python reimplementation of the original JavaScript demo repo `mfdtrade/agent-talk-2025`.

It walks through a minimal progression:

- **Step 0:** LLM call
- **Step 1:** Add a *condition* (answer-check)
- **Step 2:** Add a *tool* (SerpAPI web search)
- **Step 3:** Refactor into modules
- **Step 4:** Add **memory (read/write) + planning + loop**

## Install

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

## Configure

Copy the sample env file and add keys:

```bash
cp .env.sample .env
```

Environment variables:

- `OPENAI_API_KEY` – required for live LLM calls
- `OPENAI_MODEL` – optional (default: `gpt-4.1-mini`)
- `SERPAPI_API_KEY` – required for Step 2/4 live web search

If you don't set keys, the scripts automatically run in **mock mode** so the code still runs.

## Run the steps

```bash
python -m agent_talk.steps.step0_llm --question "What is agentic AI?"
python -m agent_talk.steps.step1_condition --question "Explain ReAct in 3 bullets"
python -m agent_talk.steps.step2_tools --question "What is the latest stable release of Python?"   --allow-web
python -m agent_talk.steps.step4_agent --goal "Find 3 reputable sources explaining ReAct and summarize them"   --allow-web --max-iters 6
```

## Tests

```bash
pytest -q
```

## Project layout

- `agent_talk/llm.py` – OpenAI wrapper + mock mode
- `agent_talk/condition.py` – answer check
- `agent_talk/tools/serpapi.py` – web search tool
- `agent_talk/memory.py` – JSON file memory (read/write)
- `agent_talk/planner.py` – make/check todo list
- `agent_talk/agent.py` – simple agent loop
- `agent_talk/steps/` – runnable step scripts
