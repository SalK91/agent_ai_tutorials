# Chapter 1: Introduction to Agentic AI

Large Language Models (LLMs) are powerful text generators, but on their own they are *not* robust problem-solvers. They lack persistent memory, cannot reliably plan over long horizons, and do not naturally interact with external environments. In practice, they may hallucinate facts, lose track of goals across long multi-step tasks, and struggle when problems require verification, tool use, or iteration.

Agentic AI reframes LLMs as components inside an *active, goal-directed system*. Instead of producing a single response and stopping, an agent operates in a loop: it reasons about a goal, takes actions (often via tools), observes outcomes, updates its internal state, and continues until the goal is achieved or a stopping condition is met. In this framing, the LLM acts as the agent’s “brain,” augmented by modules for planning, memory, tool interfaces, and self-monitoring.

This shift addresses common LLM limitations by enabling iterative, environment-aware behavior. Agents can fetch up-to-date information, verify intermediate results, persist user preferences or long-term context, and adapt their strategy when an initial attempt fails. In other words, an agent is designed to *do work*, not just *write text*.


---
# Agent = LLM + Memory + Planning + Tools + Loop
---


## From LLMs to Workflows to Agents

Before defining what makes a system “agentic,” it helps to distinguish three increasingly capable paradigms: LLMs, workflows, and agents.

### LLM-Only Systems
An LLM-only system is a single-turn or multi-turn conversation that relies primarily on the model’s internal knowledge and reasoning. Even with good prompting, the model’s behavior is bounded by:

- a finite context window,
- imperfect factual recall,
- inability to directly execute actions,
- limited reliability on long multi-step tasks.

LLM-only systems excel at drafting, summarizing, explaining, and ideating—especially when tasks do not require external verification or complex coordination.

### Workflow-Based Systems
A workflow is a *fixed orchestration* of steps defined by developers. It may call an LLM at multiple stages, route inputs through classifiers, retrieve documents, or invoke tools—but the overall sequence and decision rules are largely predetermined. Workflows are popular because they are:

- predictable (clear steps and boundaries),
- testable (each stage can be validated),
- auditable (you can log inputs/outputs per step),
- safe (restricted actions, limited autonomy).


## Examples of Workflow-Based Systems

- Prompt chaining: Break a task into a sequence of LLM calls where each step consumes the previous output. Add programmatic gates (validators) between steps to keep the process on track (e.g., outline → validate outline → draft in document creation).  

  ![alt text](images/chaining.png)  
  *Figure — Prompt chaining ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))*

- Routing: Classify the input and dispatch it to a specialized downstream prompt/toolchain. This improves performance by separating concerns (e.g., customer support: general → FAQ, refunds → policy workflow, technical → troubleshooting flow).  
  ![alt text](images/routing.png)  
  *Figure — Routing ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))*

- Parallelization: Run LLM calls concurrently and aggregate results. Two common variants are:
    - Sectioning: split a task into independent parts (e.g., summarize sections in parallel).
    - Voting: run the same task multiple times to get diverse candidates and select/merge them.  
  A common use is separating guardrails: one model generates the response while another screens for policy/safety issues.  
  ![alt text](images/parallele.png)  
  *Figure — Parallelization ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))*

- Orchestrator–workers: A central model decomposes the goal, assigns subtasks to worker models, and synthesizes results (e.g., multi-source research where each worker investigates a different source/topic).  
  ![alt text](images/Orchestrator.png)  
  *Figure — Orchestrator–workers ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))*

- Evaluator–optimizer: One model generates; another critiques; the system iterates until it meets criteria (e.g., iterative search and synthesis where the evaluator decides whether more retrieval is needed).  
  ![alt text](images/Evaluator.png)  
  *Figure — Evaluator–optimizer ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))*

Limitation: Workflows can be brittle. If inputs or environments deviate from what the pipeline anticipates, performance degrades unless developers explicitly encode additional branches, checks, and fallback logic.


### Agentic Systems
An agentic system adds a crucial capability: dynamic control. The system does not merely execute a predefined pipeline; it chooses what to do next based on the current goal, state, and observations.

A concise definition: An agentic AI system is an LLM embedded in a feedback loop (plan → act → observe → update state), where the next action is selected dynamically to achieve a goal.

![alt text](images/agent.png)
  *Figure — Agent ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))*

This does not imply “full autonomy” in every application. In practice, agentic behavior exists on a spectrum, from lightly agentic assistants (limited tool use and short plans) to highly autonomous systems (long horizons, complex coordination, multiple tools, persistent memory, and self-evaluation).



## Workflows vs Agentic AI

Because the terms are often used loosely, it is useful to draw a clear line.

### Key Differences
- Control flow
    - *Workflow:* predefined steps (often linear or branching via rules).
    - *Agent:* adaptive steps chosen at runtime.

- Decision-making
    - *Workflow:* decisions are mostly encoded by developers (routing rules, stage sequence).
    - *Agent:* decisions are made by the model/controller using current context and observations.

- Robustness to novelty
    - *Workflow:* strong on known patterns; weak on unexpected cases.
    - *Agent:* can adapt to novelty by re-planning, seeking information, or changing strategy.

- Safety and governance
    - *Workflow:* easier to constrain and audit due to fixed structure.
    - *Agent:* needs stronger guardrails (permissions, budgets, monitoring) because it can choose actions.

### When to Use Which
Use workflows when:
- the task is repeatable and well-scoped (e.g., extract → classify → draft),
- correctness requirements are high and behavior must be predictable,
- you want strict governance and minimal autonomy.

Use agentic systems when:
- tasks are open-ended, multi-step, and require adaptation (e.g., research + synthesis + verification),
- the environment is dynamic (fresh information, changing constraints),
- tool use and iterative refinement are essential.

A practical takeaway: Workflows optimize predictability. Agents optimize adaptability.

In many real systems, the best design is *hybrid*: a workflow provides structure and guardrails, while agentic submodules handle complex reasoning, planning, or tool orchestration within bounded limits.



## What Makes a System Truly Agentic?

A system is meaningfully agentic when it satisfies three conditions:

1. Goal-directed control loop: The system operates iteratively (not one-shot), maintaining a notion of progress and stopping conditions.

2. Stateful behavior: The agent maintains state across steps (short-term context, intermediate results, and often long-term memory).

3. Dynamic action selection: The system can select actions at runtime: decomposing tasks, choosing tools, seeking information, and revising plans based on observations.

This contrasts with a fixed workflow in code: instead of hard-coding every step, the agent decides “what to do next,” within constraints set by the developer.



## Agentic System Architecture

At a high level, an agentic AI system combines an LLM with three key components:

- Planning and reasoning
- Memory
- Tool interfaces

The LLM serves as the agent’s “brain,” but the supporting modules enable robust execution. Planning breaks problems into subgoals and sequences actions. Memory supports continuity across steps and sessions. Tool interfaces let the agent query external systems—search, databases, calculators, code execution, or domain APIs.

![Agentic AI architecture](images/agentic_architecture.png)  
*Figure: Overview of an agentic AI system combining planning, memory, and external tools. ([lilianweng](https://lilianweng.github.io/posts/2023-06-23-agent/))*

In this diagram, the central LLM agent uses planning (task decomposition and reflection), memory (short- and long-term storage), and tools (APIs, calculators, code) to act in the world. A typical workflow might look like:

1. Interpret the user goal
2. Break it into sub-steps
3. Retrieve relevant context from memory
4. Use tools to gather evidence or perform computation
5. Synthesize results
6. Verify, revise, and finalize



## Reasoning and Planning in Agentic AI
Agentic systems encourage models to *reason before acting* and to handle multi-step problems through explicit structure.

- Decomposition and Planning: Planning involves translating a high-level objective into manageable subgoals (e.g., “gather evidence,” “compare options,” “compute constraints,” “draft output,” “verify claims”). A plan is not static; a robust agent updates it as new information is observed.

- Reasoning + Acting with Tools:Many agent designs couple reasoning and tool use. The agent alternates between:
    
    - reasoning about what is needed next, and
    - taking an external action (search, compute, query, call an API),
then incorporating the observed result back into its state.

    This is the essence of *closed-loop* behavior: the system learns from the environment as it proceeds.

- Self-Monitoring and Recover: Agentic systems often include mechanisms for:
    - detecting uncertainty or missing information,
    - verifying intermediate outputs,
    - revising steps when contradictions appear,
    - stopping when goals are met or budgets are exceeded.

This improves reliability compared to a single-shot response, but it also introduces new challenges: if the agent’s self-evaluation is weak, it may loop or confidently pursue an incorrect path. For that reason, guardrails and verification are essential.



## Memory in Agentic AI

Memory is a cornerstone of agentic behavior because it enables continuity and learning across steps and sessions.

- Short-Term Memory: Short-term memory is the working context: the conversation history, intermediate computations, and the current plan. Because context windows are limited, agents often summarize and compress information to preserve the most important facts and decisions.

-  Long-Term Memory: Long-term memory is typically external: notes, preferences, prior decisions, or structured knowledge stored in databases or vector stores. When the agent needs relevant past information, it retrieves it and injects it into the current context.

By combining short- and long-term memory, an agent can:

- remain coherent over long tasks,
- retain user preferences,
- reuse past solutions,
- avoid repeating the same mistakes.

## Tool Use in Agentic AI

Agentic systems use tools to extend beyond text generation. Instead of relying solely on pretrained knowledge, an agent can:

- search for up-to-date information,
- run code for precise computation,
- query databases,
- call domain APIs (e.g., scheduling, finance, analytics),
- execute controlled actions in software environments.

A common pattern is LLM-as-orchestrator:

- the LLM decides *which* tool to use and *how* to call it,
- a tool executes the operation,
- the result is returned to the agent for interpretation.

This design helps ground the agent in external evidence and enables actions in the real world—while still allowing the system designer to constrain what tools are available and under what permissions.


## Reliability, Safety, and Guardrails

Agentic behavior can improve capability, but it can also amplify failures: a mistaken assumption can lead to incorrect tool calls, misleading summaries, or wasted iterations. Robust agentic systems therefore add guardrails such as:

- Verification and grounding: require evidence for factual claims, cross-check sources, use tool outputs as the “source of truth.”

- Budgets and stopping conditions: limit tool calls, time, cost, or number of iterations to prevent runaway loops.

- Permissions and sandboxing: restrict what actions tools can take; separate read-only tools from write-capable tools.

- Logging and evaluation: record traces for debugging, measure success rates, and test on representative task suites.

These controls are not optional in production-grade agent systems—they are the difference between a clever demo and a dependable product.



---

This chapter introduced the motivation for Agentic AI and clarified the progression from LLMs to workflows to agents. We defined agentic systems as LLMs embedded in a stateful control loop that dynamically selects actions—planning, using tools, observing outcomes, and updating state until a goal is reached. We then described the key architectural components: planning, memory, and tool use, along with common design patterns used to build reliable systems.

In the next chapter, we will focus on *how agents connect to tools and external resources in a standardized, scalable way*. This is where Model Context Protocol (MCP) becomes central: it provides an interoperable interface for exposing tools, resources, and prompts to agentic systems, helping reduce integration complexity and enabling more modular architectures.


## References

- Lilian Weng (2023). *LLM Powered Autonomous Agents.*
- Anthropic (2024). *Building Effective Agents*
- Agentic AI: A Progression of Language Model Usage (2025) ([webinar link](https://www.youtube.com/watch?v=kJLiOGle3Lw))


