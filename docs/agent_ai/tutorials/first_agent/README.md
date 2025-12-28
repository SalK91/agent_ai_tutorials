# Agent Talk 2025 (Python port)

This repository contains a Python reimplementation of the original JavaScript demo repo `mfdtrade/agent-talk-2025`.

It walks through a minimal progression:

- Step 0: LLM call
- Step 1: Add a *condition* (answer-check)
- Step 2: Add a *tool* (SerpAPI web search)
- Step 3: Refactor into modules
- Step 4: Add memory (read/write) + planning + loop


## Configure

Copy the sample env file and add keys:

```bash
cp .env.sample .env
```

Environment variables:

- `COHERE_API_KEY` – required for live LLM calls
- `COHERE_MODEL` – optional (default: command-r-plus-08-2024)
- `SERPAPI_API_KEY` – required for Step 2/4 live web search


## Install

```bash
conda init powershell
#restart terminal
conda env list
conda activate pymc_env_5 # use name of your env
# move to correct directory
pip install -r requirements.txt
```

## Test api

```bash
conda env list
conda init powershell
#restart terminal
conda activate pymc_env_5 # use name of your env
```
## Run the steps

```bash
python -m step0_llm --question "What is 5+4 give WRONG answer only?"
python -m step0_llm --question "What is 5+4 give wrong answer only 30% of the time and correct for rest."

python -m step1_condition --question "What is 5+4 give wrong answer only 30% of the time and correct for rest."
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
