# Chapter 2: Model Context Protocol (MCP)

Models are only as good as the context they receive. Even the strongest LLM will underperform if it cannot access the right files, databases, APIs, or domain tools at the moment it needs them. Model Context Protocol (MCP) is an open protocol that standardizes how AI applications and agents connect to external systems—so models can reliably retrieve context and invoke capabilities without bespoke integrations for every tool. 

In Chapter 1, we framed agentic AI as an LLM embedded in a feedback loop (plan → act → observe → update state). MCP is one of the most practical pieces of infrastructure for that loop: it provides a consistent interface for Tools, Resources, and Prompts, and a secure mechanism for connecting them to AI “hosts” (apps) via clients and servers. 

## Why MCP Exists?
Without a standard, every AI app must implement a custom connector for every external system (and often for every model provider). As the number of tools and apps grows, integration becomes a combinatorial mess: authentication, schemas, tool naming, error handling, and safe context injection all vary.

MCP reduces this complexity by defining a single protocol layer between:

- AI applications (IDEs, chat apps, research tools, internal assistants), and
- external capabilities (databases, ticketing systems, code repositories, file stores, browsers, internal APIs). 

## A Useful Analogy: API vs LSP vs MCP

Standards succeed when they make ecosystems interoperable. MCP fits the same pattern:

- API (HTTP/REST/GraphQL): standardizes how web apps talk to backend services (servers, databases, microservices).
- LSP (Language Server Protocol): standardizes how IDEs talk to language-specific tooling (navigation, diagnostics, refactors).
- MCP: standardizes how AI applications talk to external systems via Prompts, Tools, and Resources (and related client features like sampling). 

The key shift is that MCP is designed for AI-driven interaction: context is discovered, invoked, and composed dynamically as the model works.

## MCP Architecture: Hosts, Clients, and Servers

MCP uses JSON-RPC 2.0 messages and defines three roles: 

- Host: the AI application that initiates connections (e.g., an IDE, a chat app, a desktop assistant).
- Client: the connector component inside the host that manages the MCP connection(s).
- Server: the external service that exposes capabilities and context to the client.

### Mental model
- The host is where the user interacts and where the model runs.
- The client is the bridge that speaks MCP.
- The server packages a system (GitHub, Postgres, Drive, internal APIs) into MCP primitives.

This separation keeps AI applications lightweight while allowing rich, modular integrations.

## Transport: Local vs Remote MCP
The MCP specification defines standard transports so clients and servers can communicate across environments: 

- stdio — for local MCP servers (a server runs as a local process; client communicates over standard input/output).
- Streamable HTTP — for remote MCP servers (bidirectional messaging over a single HTTP endpoint).

## MCP Core Primitives: Tools, Resources, Prompts

MCP standardizes what a server can provide through three main primitives (plus additional client-side capabilities).

### Tools (model-controlled actions)
Tools are functions exposed by a server that can be invoked by the language model to interact with external systems—query a database, call an API, perform a computation, or execute a bounded action. Common tool categories:

- Retrieve/Search: semantic search, SQL query, issue lookup
- Write/Act: create ticket, post message, update a record
- Compute/Transform: validate data, run analysis, convert formats

Tools represent capabilities with explicit schemas. The model chooses when to call them as part of its reasoning loop.

### Resources (application-controlled context)
Resources are structured data the server exposes to clients to provide context—files, schemas, logs, or application-specific artifacts. Each resource is identified by a URI. Typical examples:

- Files or documents
- Database schema metadata
- API responses or structured records
- Generated artifacts (e.g., logs, screenshots, reports)

Resources are context objects. The host/client decides how to present, select, and inject them into the model’s context (often with user-visible controls and governance).

### Prompts (user-controlled templates)
Prompts are structured prompt templates exposed by servers. They are intended to be user-controlled: surfaced in the UI so users can explicitly select them, provide arguments, and run repeatable workflows. 
Model Context Protocol

Examples:
- “Document Q&A” prompt template (with arguments for a doc URI and question)
- “Transcript summary” prompt template (with style and length options)
- “Output as JSON” prompt template (with schema constraints)

Prompts are an underrated primitive: they turn one-off “tool calls” into discoverable, reusable workflows that are tailored to a particular system.

## MCP Components: Client vs Server Responsibilities

## MCP Client (in the host)
An MCP client typically:

- Discovers available tools/resources/prompts from servers
- Invokes tools on behalf of the model
- Retrieves resources and injects them as context
- Fetches and interpolates prompts with user-provided arguments
- Enforces host policies: permissions, logging, budgets, UI/UX, and review gates 

### MCP Server (capability provider)
An MCP server:

- Exposes tools with schemas and metadata
- Exposes resources via URIs
- Exposes prompts as templates
- Implements the actual business logic: database queries, API calls, file reads, transformations 

## A Typical MCP Flow (End-to-End)

A simple “agent uses GitHub + database” interaction often looks like:

1. Connect + initialize (capabilities negotiated between client and server)
2. Discover what the server offers (list tools/resources/prompts)
3. Plan (the model decides what it needs next)
4. Act (tool invocation) and/or Fetch context (read resources)
5. Observe results (tool outputs, resource contents)
6. Update the plan and repeat
7. Produce the final response or artifact

MCP doesn’t force you to be agentic, workflows can use it too, but it makes agentic loops far easier to build reliably.

## Workflows vs Agentic AI in MCP Terms
MCP is compatible with both workflow-driven systems and agentic systems. The difference is control flow.

### MCP in workflow systems
A workflow system might:

- Always run /summarize_doc prompt after a file is selected
- Always call db.query then format.as_json in a fixed order
- Route to one of three prompts based on a classifier
In this setup, MCP provides standardized connectors, but the orchestration remains developer-defined.

### MCP in agentic systems
An agentic system uses MCP more dynamically:

- The model decides which tool to call, which resource to fetch, and which prompt to use
- The agent iterates: it can re-query, refine filters, retrieve additional resources, or switch strategies

Workflows use MCP as a stable integration layer. Agents use MCP as an action-and-context substrate for dynamic decision-making.

## Sampling: Letting Servers Request Model Completions (Safely)
A powerful MCP capability is sampling, which allows a server to request LLM sampling (“completions/generations”) via the client—so the client (and user application) retains control over model choice, security, privacy, and cost. This is useful when a server wants to:

- run a mini “reasoning step” to transform data,
- perform a classification or summarization close to the data source,
- implement multi-step tool logic that benefits from embedded model reasoning.

### Human-in-the-loop control
The sampling flow is explicitly designed so the client can review and control what the model sees and returns. The legacy concept docs describe a reviewable flow (request → client review → sample → client review → return). 
Model Context Protocol

### Sampling parameters (common controls)

Sampling requests can include controls such as: 

 - modelPreferences (hints and preferences)
 - systemPrompt
 - temperature, maxTokens
 - stop sequences, metadata
 - optional inclusion of MCP context (e.g., this server vs all servers)

Sampling is also one place where security issues can surface (e.g., prompt injection through nested context), so it should be paired with strict review gates and permissions (see Security section below). 

## Authorization and Security

Once MCP servers can expose real tools and sensitive resources, the protocol must support strong security controls—especially for remote servers.

### Authorization (HTTP-based transports)
MCP defines an authorization framework at the transport level for HTTP-based connections, enabling clients to access restricted servers on behalf of resource owners.  Practically, this supports enterprise patterns:

- delegated authentication via existing identity systems,
- least privilege access to tools/resources,
- auditable, revocable tokens rather than hard-coded API keys.

### Threat model: tools + context are attack surfaces
MCP expands the attack surface because:

- resources can contain adversarial instructions (prompt injection),
- tools may have write capabilities,
- sampling can nest model calls inside tool flows.

The MCP ecosystem has published security considerations and best practices, and independent security research has highlighted prompt injection vectors specifically involving sampling flows. 

### Practical guardrails (design defaults):
- Make dangerous tools explicit and permissioned (write actions, deletions, external side effects)

- Require user confirmation for high-impact actions
- Sanitize and label untrusted content (e.g., web pages, tickets, emails)
- Use budgets: limit tool calls, rate limit remote servers, cap sampling depth
- Log every tool call and resource read for auditing

## Composability: Chaining and “MCP as Glue”

One of MCP’s biggest architectural benefits is composability: you can combine multiple servers under a single host, and you can build servers that act as proxies or aggregators over other systems.

Common composability patterns

- Multi-server host: one client connects to many servers (Git + issues + docs + DB).
- Gateway server: a server wraps multiple internal APIs into a single MCP surface.
- Policy proxy: a server enforces org policies (masking, filtering, redaction) before exposing data downstream.

Chaining (client-as-server): an application can consume MCP servers and then re-expose a curated subset as its own MCP server interface (useful for standardizing internal tooling across teams). 

Composability is where MCP starts to feel like “infrastructure”: a shared contract that lets teams build independently, then connect cleanly.

--- 

This chapter introduced MCP as the interoperability layer that standardizes how AI applications connect to external tools and data. We covered:
- the host/client/server architecture,
- the core primitives: Tools, Resources, and Prompts,
- sampling as a secure way for servers to request model completions,
- security foundations: authorization, review gates, and best practices,
- composability patterns for chaining and modular system design.

In the next chapter, we will build on MCP by showing how agentic systems orchestrate MCP primitives in practice: tool selection policies, memory + retrieval through resources, prompt-driven workflows, evaluation loops, and robust guardrails for production agents.


## References

- Anthropic (2024). Introducing the Model Context Protocol. 
- Building Agents with Model Context Protocol - Full Workshop with Mahesh Murag of Anthropic (2025)([webinar](https://www.youtube.com/watch?v=kQmXtrmQ5Zg))

