# Agent Talk 2025 (Python port)

This repository contains a Python reimplementation of the original JavaScript demo repo `mfdtrade/agent-talk-2025`.

It walks through a minimal progression:

- Step 0: LLM call
- Step 1: Add a *condition* (answer-check)
- Step 2: Add a *tool* (SerpAPI web search)
- Step 3: Add memory (read/write) + planning + loop


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

## Run the steps

```bash
python -m step0_llm --question "What is 5+4?"
python -m step1_condition --question "What is 5+4?"
python -m step2_tools --question "What is the latest stable release of Python?"   --allow-web
python -m step3_agent --goal "Find 3 best spots to watch fireworks in London for New-Year 2026 near Isle of dock based on latest articles in news"   --allow-web --max-iters 6
```

## Tests

```bash
pytest -q
```

## Project layout

- `utils/llm.py` – Cohere wrapper 
- `utils/condition.py` – answer check
- `utils/serpapi.py` – web search tool
- `utils/memory.py` – JSON file memory (read/write)
- `utils/planner.py` – make/check todo list
- `utils/agent.py` – simple agent loop
