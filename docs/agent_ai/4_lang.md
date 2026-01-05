# LangChain vs LangGraph vs LangSmith

### LangChain -> build the app
- Framework for building LLM applications
- Provides tools: prompts, chains, agents, memory, RAG, integrations, etc.
- Helps connect models to data sources, APIs, databases
- Focus: Build and orchestrate AI workflows
- Best for: Chatbots, RAG apps, agents, LLM pipelines

### LangGraph -> design complex stateful logic (graphs, loops, multi-agent flow)
- Extension of LangChain for stateful, multi-step logic
- Uses graph structure (nodes + edges) instead of simple linear chains
- Enables loops, branching, checkpoints, persistence
- Focus: Control flow & complex agent state management
- Best for: Multi-agent systems, long conversations, workflows with decision paths

### LangSmith -> monitor & debug the app in development or production
- Debugging & monitoring platform (not a chain builder)
- Logs, traces, evaluates, monitors cost, latency, errors
- Helps improve prompt quality and agent performance
- Focus: Observe, test, evaluate, and monitor production LLM apps
- Best for: Debugging, performance analytics, experiment tracking


https://academy.langchain.com/courses/foundation-introduction-to-langchain-python

### References:
1. LangChain Academy: https://academy.langchain.com/collections