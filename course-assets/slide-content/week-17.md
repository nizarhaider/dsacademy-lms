# Week 17: AI Agents and LangGraph Workflows

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who understand tools, validation, RAG, and tracing  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 17 presentation and related media.

---

## Slide 1 - Use a Workflow When the Steps Are Known

### Teaching purpose

Distinguish deterministic workflows from agent choice.

### Learner-facing content

A **workflow** follows declared steps and branches.

An **agent** uses a model to choose among allowed actions based on state and observations.

Use deterministic code when the next step is known. Grant model choice only where it adds value, such as choosing which read-only search tool can answer an unfamiliar question.

More autonomy increases evaluation, permission, cost, and stopping requirements.

### Worked example

Invoice processing:

`validate -> extract -> human review -> save`

These steps are known, so a workflow is appropriate.

Research assistant:

The model may choose policy search or product search based on the question, within a bounded tool set.

### Code example

```python
if request.type == "invoice":
    next_step = "extract"
else:
    next_step = "clarify"
```

Expected output:

```text
An explicit branch without an unnecessary model decision.
```

### Visual description

A fixed workflow and a bounded agent loop appear side by side with increasing autonomy and risk.

### Instructor notes

Challenge every proposed agent: which choice cannot be written as a clear rule?

### Notebook connection

The LangGraph quickstart shows both a workflow and a tool-using agent.

### Sources

- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [AI Bootcamp: LangGraph Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/29.langgraph-quickstart.ipynb)

---

## Slide 2 - State, Nodes, and Edges Define a Graph

### Teaching purpose

Teach the three core LangGraph concepts.

### Learner-facing content

**State** is the typed record describing the current run.

A **node** is a function that reads state and returns state updates.

An **edge** determines which node runs next.

`START` represents graph input and `END` represents termination.

Store raw, reusable data in state rather than only formatted prose. Every field should have an owner and meaning.

### Worked example

State:

```text
question, retrieved_docs, draft, approved, attempts
```

Node `retrieve` adds documents. Node `draft` adds an answer. An edge routes to review if approval is required.

### Code example

```python
class State(TypedDict):
    question: str
    documents: list[Document]
    answer: str | None
    attempts: int
```

Expected output:

```text
A typed state schema shared by graph nodes.
```

### Visual description

A state record moves through nodes; each node highlights only the fields it reads and updates.

### Instructor notes

Explain that state is application memory for the run, not hidden model memory.

### Notebook connection

The notebook defines state before adding nodes and edges.

### Sources

- [LangGraph: Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangGraph: Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)

---

## Slide 3 - A Node Should Perform One Inspectable Job

### Teaching purpose

Teach decomposition and node contracts.

### Learner-facing content

A good node has:

- declared state inputs;
- one responsibility;
- typed outputs;
- bounded external calls;
- visible errors;
- trace span;
- retry policy only when appropriate.

Small nodes make failures and approvals easier to locate. Do not place retrieval, generation, tool execution, and database write inside one opaque node.

### Worked example

Node `retrieve_policy`:

Input: question and user authorization  
Action: authorized retrieval  
Output: ranked documents and retrieval metadata  
Failure: denied, timeout, or no evidence

It does not generate an answer.

### Code example

```python
def retrieve_policy(state: State):
    docs = retriever.invoke(state["question"])
    return {"documents": docs}
```

Expected output:

```text
A state update containing documents while preserving other state fields.
```

### Visual description

One oversized node is decomposed into validate, retrieve, draft, review, and publish nodes.

### Instructor notes

Ask what evidence proves each node succeeded.

### Notebook connection

Learners inspect each quickstart node as a state transformation.

### Sources

- [LangGraph: Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [AI Bootcamp: LangGraph Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/29.langgraph-quickstart.ipynb)

---

## Slide 4 - Edges Make Routing Explicit

### Teaching purpose

Explain fixed and conditional transitions.

### Learner-facing content

A fixed edge always routes to the same node.

A **conditional edge** inspects state and chooses from declared destinations.

Routing functions should return only allowed routes and should be tested independently. Important policy decisions, such as whether a user can write data, should be deterministic code rather than model preference.

### Worked example

After retrieval:

- documents found -> `draft_answer`
- no documents -> `insufficient_evidence`
- authorization denied -> `denied`

All three outcomes are explicit terminal or next states.

### Code example

```python
def route_after_retrieval(state: State):
    if state["denied"]:
        return "denied"
    return "draft" if state["documents"] else "insufficient"
```

Expected output:

```text
One allowed node name determined from typed state.
```

### Visual description

A retrieval node branches into draft, insufficient, and denied paths with labelled conditions.

### Instructor notes

Separate a model classification used as evidence from the code that enforces permissions.

### Notebook connection

The quickstart workflow adds conditional edges after node results.

### Sources

- [LangGraph: Use the Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)
- [LangGraph: Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

---

## Slide 5 - Tools Turn Model Choices into Proposed Actions

### Teaching purpose

Connect Week 13 tool contracts to agent state.

### Learner-facing content

An agent model may propose:

- tool name;
- structured arguments;
- reason reflected in its current messages.

The application:

1. parses arguments;
2. authorizes the tool and scope;
3. applies time and resource limits;
4. executes;
5. records the observation in state;
6. routes to the next decision.

Tool results are untrusted external data and may contain errors or injection text.

### Worked example

Agent proposes `search_policy(query="refund annual plan")`.

Application checks that search is read-only and tenant-filtered, then stores returned chunks and provenance. It rejects a proposed `delete_policy` because that tool is not in the allowed set.

### Code example

```python
args = SearchArgs.model_validate(tool_call.args)
authorize(user, "search_policy", args)
observation = search_policy(**args.model_dump())
```

Expected output:

```text
A bounded observation or a structured denied/error result.
```

### Visual description

Model proposal passes through schema, authorization, execution, and observation stages before re-entering state.

### Instructor notes

Repeat that tool schemas describe valid shape but do not grant permission.

### Notebook connection

The agent quickstart alternates a model node with a tool node.

### Sources

- [LangGraph: Tool Calling](https://docs.langchain.com/oss/python/langgraph/agentic-rag)
- [Model Context Protocol: Tools](https://modelcontextprotocol.io/docs/concepts/tools)

---

## Slide 6 - The Agent Loop Is Action, Observation, and Decision

### Teaching purpose

Explain iterative tool use and why it needs limits.

### Learner-facing content

A tool-using agent loop:

1. inspect goal and current state;
2. choose an allowed action or finish;
3. execute through application controls;
4. receive an observation;
5. update state;
6. choose again.

The observation may resolve the question, reveal missing information, or produce an error.

Every loop needs an explicit route to `END`.

### Worked example

Step 1: search policy -> no matching chunk  
Step 2: search product documentation -> supporting chunk found  
Step 3: answer with citation -> finish

Total tool calls `2`, model decisions `3`.

### Code example

```python
def should_continue(state):
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END
```

Expected output:

```text
The graph routes to tools only when the latest model output proposes a call.
```

### Visual description

A bounded loop connects model decision, tool execution, observation, and finish.

### Instructor notes

Ask what state proves the task is complete. Do not rely on token exhaustion.

### Notebook connection

Learners trace every loop iteration in the LangGraph agent example.

### Sources

- [LangGraph: Use Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)
- [AI Bootcamp: LangGraph Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/29.langgraph-quickstart.ipynb)

---

## Slide 7 - Checkpoints Make State Durable

### Teaching purpose

Explain persistence, thread IDs, and resume behaviour.

### Learner-facing content

A **checkpoint** is a saved snapshot of graph state at an execution boundary.

Checkpoints support:

- recovery after failure;
- multi-turn memory;
- human approval pauses;
- replay and debugging;
- resuming long-running work.

A **thread ID** identifies which persisted state to load. Access to checkpoints must be authorized because state may contain sensitive data.

### Worked example

Graph completes retrieve and draft, then pauses for approval.

Checkpoint stores question, documents, draft, and status. The process can restart and resume from that state instead of rerunning retrieval and generation.

### Code example

```python
config = {"configurable": {"thread_id": "request-123"}}
result = graph.invoke(initial_state, config)
```

Expected output:

```text
State snapshots associated with request-123 in the configured checkpointer.
```

### Visual description

Graph steps leave checkpoint markers. A restart resumes from the latest successful marker.

### Instructor notes

Explain retention, encryption, and tenant isolation for persisted state.

### Notebook connection

Learners add an in-memory checkpointer for the lab and document production storage requirements.

### Sources

- [LangGraph: Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph: Overview](https://docs.langchain.com/oss/python/langgraph/overview)

---

## Slide 8 - Retries Must Be Node-Specific and Resume-Safe

### Teaching purpose

Teach transient failures, idempotency, and side-effect protection.

### Learner-facing content

Retry only a node whose operation can safely be repeated.

**Idempotent** means repeating the same operation has the same intended effect as running it once.

- read-only search is often retryable;
- charging a card or sending an email may duplicate side effects;
- model calls may produce different outputs on retry;
- validation failures need correction, not blind retry.

Record attempts and cap them.

### Worked example

Search times out: retry up to `3` attempts.  
Email send times out after the server may have accepted it: check an idempotency key or delivery status before retrying.

### Code example

```python
workflow.add_node(
    "search",
    search_node,
    retry_policy=RetryPolicy(max_attempts=3),
)
```

Expected output:

```text
Only the search node receives the bounded retry policy.
```

### Visual description

Read-only search has a retry loop; write action has an idempotency and confirmation gate.

### Instructor notes

Ask what observable state distinguishes “failed before action” from “response lost after action.”

### Notebook connection

The lab simulates a transient search failure and confirms attempt count.

### Sources

- [LangGraph: Fault Tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)
- [AWS: Retry with Backoff](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html)

---

## Slide 9 - Human Approval Is a State Transition

### Teaching purpose

Explain interrupt, review, edit, resume, and audit.

### Learner-facing content

Use human approval before high-impact or uncertain actions.

The graph should:

1. prepare a proposal;
2. persist state;
3. interrupt;
4. show evidence and proposed action;
5. accept approve, reject, or edited input;
6. validate human input;
7. resume from the checkpoint;
8. record reviewer and decision.

Approval must occur before the side effect.

### Worked example

Agent drafts an email and proposed recipients. The graph pauses. Reviewer removes one recipient and approves the edited draft. Only then may the send node execute.

### Code example

```python
decision = interrupt({
    "draft": state["draft"],
    "recipients": state["recipients"],
})
```

Expected output:

```text
The graph pauses with JSON-serializable review data until resumed.
```

### Visual description

A workflow stops at a human-review gate and resumes along approved, edited, or rejected paths.

### Instructor notes

Explain why side effects before an interrupt can be repeated on resume.

### Notebook connection

Learners add one approval interrupt to a write-capable mock action.

### Sources

- [LangGraph: Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph: Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)

---

## Slide 10 - Stopping Conditions Bound Time, Cost, and Risk

### Teaching purpose

Define explicit execution limits and permission scopes.

### Learner-facing content

Set:

- maximum graph steps;
- maximum attempts per node;
- maximum tool calls;
- wall-clock timeout;
- token and cost budget;
- allowed tool set;
- argument and result-size limits;
- terminal conditions for success, denial, insufficient evidence, and failure.

An agent must be able to stop without producing a successful answer.

### Worked example

Limits:

`max_steps=8`, `max_tool_calls=3`, `budget=$0.05`, `timeout=30s`

After three searches with no supporting evidence, route to `insufficient_evidence` rather than search indefinitely.

### Code example

```python
if state["tool_calls"] >= 3 or state["cost"] >= 0.05:
    return Command(update={"status": "budget_exhausted"}, goto=END)
```

Expected output:

```text
A terminal state reached before the execution exceeds its bounds.
```

### Visual description

The agent loop is surrounded by step, call, time, token, cost, and permission limits.

### Instructor notes

Treat recursion limits as a final guard, not the only meaningful stopping rule.

### Notebook connection

The lab tests successful, insufficient, denied, timeout, and budget-exhausted endings.

### Sources

- [LangGraph: Create and Control Loops](https://docs.langchain.com/oss/python/langgraph/use-graph-api#create-and-control-loops)
- [LangGraph: Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

---

## Slide 11 - A Minimal LangGraph Is Explicit Python

### Teaching purpose

Assemble state, nodes, edges, and compilation.

### Learner-facing content

Build order:

1. define typed state;
2. implement small node functions;
3. add nodes;
4. add fixed and conditional edges;
5. compile with runtime controls;
6. invoke with initial state and configuration;
7. inspect final state and trace.

Compilation checks graph structure. It does not prove node logic or safety.

### Worked example

`START -> retrieve -> route`

- documents -> answer -> END
- no documents -> insufficient -> END

There is no loop because one retrieval is enough for this workflow.

### Code example

```python
builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("answer", answer)
builder.add_edge(START, "retrieve")
builder.add_conditional_edges("retrieve", route)
graph = builder.compile()
```

Expected output:

```text
A compiled graph whose allowed paths match the declared edges.
```

### Visual description

The code lines map directly to a small graph diagram and typed state updates.

### Instructor notes

Have learners draw the graph before writing builder calls.

### Notebook connection

This prepares learners to read the quickstart workflow and agent graphs.

### Sources

- [LangGraph: Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [AI Bootcamp: LangGraph Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/29.langgraph-quickstart.ipynb)

---

## Slide 12 - Guided Lab: Build a Bounded Research Workflow

### Teaching purpose

Set a practical LangGraph assessment.

### Learner-facing content

Build a policy-research graph with:

1. typed state;
2. validate, route, retrieve, answer, and finish nodes;
3. one deterministic route;
4. one model-selected read-only tool;
5. argument validation and authorization;
6. observations stored with provenance;
7. checkpoint persistence;
8. bounded retries for transient search failure;
9. human approval before a mock publish action;
10. maximum steps, calls, time, and cost;
11. complete tracing;
12. tests for success, insufficient evidence, denial, timeout, and rejected approval.

### Worked example

Trace:

`validate -> retrieve -> answer -> review -> rejected -> END`

The final status is `rejected`; no publish side effect occurs.

### Code example

```python
result = graph.invoke(
    {"question": question, "tool_calls": 0, "status": "started"},
    {"configurable": {"thread_id": request_id}, "recursion_limit": 10},
)
```

Expected output:

```text
A typed final or interrupted state within the declared execution limit.
```

### Visual description

The final graph diagram labels state, branches, tool loop, checkpoint, approval, and terminal statuses.

### Instructor notes

Require failure-path demonstrations before accepting the success path.

### Notebook connection

Complete `29.langgraph-quickstart.ipynb`; use `18.langgraph-basics.ipynb` only as an optional secondary exercise.

### Sources

- [AI Bootcamp: LangGraph Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/29.langgraph-quickstart.ipynb)
- [AI Bootcamp: LangGraph Basics](https://github.com/curiousily/AI-Bootcamp/blob/master/18.langgraph-basics.ipynb)
