---
name: "mcp-server-designer"
description: "Use when the user wants to design, plan, or review an MCP server before or during implementation, including tool shape, transport choice, auth, pagination, filtering, error handling, and integration boundaries. Do not use for generic API integration advice or for creating Codex skills."
---

# MCP Server Designer

Design an MCP server that is easy for agents to use and easy to maintain. Keep the focus on protocol-aware server shape, tool granularity, and the tradeoffs that affect agent behavior in practice.

Use this skill when the user is:

- planning a new MCP server
- refactoring an existing MCP server
- deciding which tools, resources, or prompts the server should expose
- choosing between stdio, streamable HTTP, or another deployment shape
- trying to make an MCP integration more reliable for agents

## Do Not Use For

- generic REST or GraphQL API design that is not MCP-specific
- implementation-only coding work with no need for protocol design
- authoring Codex skills or subagents
- broad research into a service domain without an MCP server decision to make

## Workflow

1. Frame the server job before touching the tool list.
   - Identify the user task the server must support.
   - Name the primary actors, expected inputs, and expected outputs.
   - Stop if the underlying use case is unclear.

2. Design for the agent first, not the raw API.
   - Prefer a small set of high-value tools over a one-to-one endpoint mirror.
   - Make tool names action-oriented, specific, and easy to scan.
   - Group related actions only when the grouping keeps tool calls simple.

3. Choose the right MCP surface area.
   - Use tools for actions and decisions.
   - Use resources for stable, readable state or documents.
   - Use prompts only when a guided workflow is genuinely better than a tool.
   - Avoid exposing surface area that an agent cannot use safely.

4. Plan protocol details explicitly.
   - Choose the transport that best fits the deployment and auth model.
   - Decide how authentication is handled and where secrets live.
   - Specify pagination, filtering, and search behavior for list-heavy operations.
   - Define error shapes that tell the agent what to fix next.

5. Design each tool to be easy to call and hard to misuse.
   - Keep input schemas narrow and explicit.
   - Use stable identifiers rather than ambiguous natural language when possible.
   - Return concise results with enough context for the next step.
   - Prefer predictable outputs over overloaded responses.

6. Check operational fit.
   - Note rate limits, retries, idempotency, and latency-sensitive paths.
   - Call out any write actions that need confirmation or guardrails.
   - Separate read-only workflows from destructive ones when the risk differs.

7. Produce a concrete server plan.
   - Summarize the recommended tool set.
   - State the transport and auth model.
   - Call out the main failure modes and how the server should surface them.
   - List any open questions or implementation blockers.

## Output Expectations

Return a short server design brief with:

- the server's owned job
- the proposed tools, resources, or prompts
- the transport and auth choice
- pagination, filtering, and error-handling decisions
- integration risks or unresolved questions

If the user asks for implementation guidance, keep the answer one step ahead of code and stay at the design level unless they explicitly ask for files.

## Guardrails

- Do not turn this into generic API client advice.
- Do not mirror every upstream endpoint unless that is clearly the best agent interface.
- Do not hide auth, pagination, or error handling behind vague implementation notes.
- Do not replace the existing skill-authoring workflow.
- Do not assume a single transport or auth model fits every server.
