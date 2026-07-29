# Week 18: Production AI Capstone

**Status:** PRODUCTION AUTHORIZED

**Audience:** Learners who completed the Python, ML, deployment, LLM, RAG, and agent workflow sequence  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 18 presentation and related media.

---

## Slide 1 - Start with a Testable User Need

### Teaching purpose

Frame the capstone as a production problem, not a framework demonstration.

### Learner-facing content

A **requirement** is a testable statement of needed behaviour or constraint.

Define:

- user and decision;
- input and expected output;
- quality threshold;
- unsupported and denied behaviour;
- latency target;
- cost limit;
- privacy and security constraints;
- deployment environment;
- owner and success measure.

Choose a narrow problem whose evidence and failures can be demonstrated.

### Worked example

Need: `Support staff must answer policy questions using the current approved handbook.`

Acceptance:

- citation-supported answer or insufficient evidence;
- no cross-tenant sources;
- p95 latency under `3s`;
- estimated cost under `$0.02` per request;
- zero unsupported critical claims in the reviewed test set.

### Code example

```python
acceptance = {
    "groundedness_min": 0.95,
    "p95_latency_ms_max": 3000,
    "cost_usd_max": 0.02,
    "cross_tenant_failures_max": 0,
}
```

Expected output:

```text
A measurable contract used throughout design and evaluation.
```

### Visual description

A user need expands into quality, safety, latency, cost, and operational acceptance criteria.

### Instructor notes

Reject “build an AI chatbot” as a requirement. Ask what user decision improves and how it will be measured.

### Notebook connection

The selected capstone notebook supplies technical patterns, not the project requirements.

### Sources

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)

---

## Slide 2 - Architecture Assigns Responsibilities to Components

### Teaching purpose

Teach architecture as decisions and interfaces.

### Learner-facing content

An **architecture** identifies components, responsibilities, interfaces, and constraints.

A capstone may include:

- web or API client;
- request validation;
- workflow state;
- retrieval and vector store;
- model provider;
- structured output;
- authorized tools;
- database;
- observability;
- deployment infrastructure.

Use the fewest components that satisfy requirements. Every additional service adds failure and cost.

### Worked example

Policy assistant:

`Client -> FastAPI -> LangGraph workflow -> retriever -> model -> validated answer`

Documents enter through a separate ingestion job. The online API cannot modify source policies.

### Code example

```text
Online path: request -> validate -> retrieve -> answer -> verify -> respond
Offline path: source -> parse -> approve -> chunk -> embed -> index
```

Expected output:

```text
Separate online and ingestion responsibilities with explicit interfaces.
```

### Visual description

An architecture diagram separates offline ingestion, online request flow, storage, and observability.

### Instructor notes

Ask who owns every datum and which component may modify it.

### Notebook connection

Learners adapt only notebook components needed by the selected architecture.

### Sources

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)

---

## Slide 3 - Data Flow Reveals Trust Boundaries

### Teaching purpose

Map data origin, transformations, storage, and permissions.

### Learner-facing content

A **data-flow diagram** shows:

- data sources;
- movement between components;
- transformations;
- storage;
- external providers;
- trust boundaries;
- authentication and authorization points;
- sensitive fields;
- retention and deletion.

Untrusted user input, retrieved documents, model output, and tool results all require validation at their boundaries.

### Worked example

Policy documents are approved internally, but their extracted text may contain parser errors. User question is untrusted. Model output is untrusted. Final response is released only after schema, citation, and authorization checks.

### Code example

```text
[User] --untrusted question--> [API validation]
[Retriever] --authorized chunks--> [Model]
[Model] --untrusted draft--> [Output validation]
```

Expected output:

```text
Every boundary has an owner and required check.
```

### Visual description

Data arrows cross labelled public, application, provider, and storage trust zones.

### Instructor notes

Make learners identify secrets and personal data before discussing frameworks.

### Notebook connection

Tool and RAG notebook code is placed only inside approved trust boundaries.

### Sources

- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Slide 4 - Select Models from Evaluation Evidence

### Teaching purpose

Require baseline and measured model selection.

### Learner-facing content

Model selection should compare:

- baseline;
- at least two suitable candidates;
- quality on the same test cases;
- structured-output and tool capability;
- latency and token use;
- cost;
- data policy;
- deployment fit.

Record exact model identifiers and configuration. A larger model is not automatically the correct production choice.

### Worked example

Candidate A: groundedness `0.97`, p95 `4.5s`, cost `$0.03`  
Candidate B: groundedness `0.95`, p95 `2.2s`, cost `$0.01`

If minimum groundedness is `0.95`, p95 maximum `3s`, and cost maximum `$0.02`, only B passes all constraints.

### Code example

```python
passing = results[
    (results.groundedness >= 0.95)
    & (results.p95_ms <= 3000)
    & (results.cost <= 0.02)
]
```

Expected output:

```text
Only candidates satisfying every hard requirement.
```

### Visual description

A requirements gate filters model experiment rows; the selected model is traceable to evidence.

### Instructor notes

Keep current vendor and price decisions in configuration and reports, not permanent slide claims.

### Notebook connection

Provider comparison from Week 14 becomes a capstone selection report.

### Sources

- [LangSmith: Evaluation](https://docs.langchain.com/langsmith/evaluation)
- [LiteLLM Documentation](https://docs.litellm.ai/)

---

## Slide 5 - Use Structured Output, RAG, and Tools Only When Needed

### Teaching purpose

Make capability choices requirement-driven.

### Learner-facing content

Use **structured output** when downstream code needs fields and types.

Use **RAG** when answers require current, private, or cited evidence.

Use **tools** when the system must retrieve live data or perform a bounded operation.

Use a **workflow** when steps are known. Use agent choice only when deciding among allowed actions adds measurable value.

Each capability needs its own validation and evaluation.

### Worked example

Policy assistant:

- structured output: answer, status, citation IDs;
- RAG: approved handbook;
- tool: read-only ticket lookup only if ticket context is required;
- no write-capable agent because the requirement is answer support.

### Code example

```python
class Answer(BaseModel):
    status: Literal["supported", "insufficient", "denied"]
    answer: str | None
    citation_ids: list[str]
```

Expected output:

```text
A typed outcome that represents success and safe non-success states.
```

### Visual description

Requirements connect to optional capability blocks; unused blocks remain outside the architecture.

### Instructor notes

Challenge decorative agent or tool additions that lack an acceptance criterion.

### Notebook connection

Learners select one primary capstone notebook and use others only for justified components.

### Sources

- [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)

---

## Slide 6 - Workflow State Makes Behaviour Inspectable

### Teaching purpose

Define the capstone's state machine and terminal statuses.

### Learner-facing content

Capstone state should track:

- request and user context;
- validated inputs;
- retrieved evidence;
- model outputs;
- tool proposals and observations;
- attempts, tokens, latency, and cost;
- approvals;
- current status;
- final result and errors.

Declare terminal statuses such as `supported`, `insufficient`, `denied`, `rejected`, `timeout`, and `failed`.

### Worked example

Route:

`validate -> retrieve`

- denied -> END
- no evidence -> insufficient -> END
- evidence -> generate -> verify
- unsupported draft -> one bounded repair
- supported -> END

### Code example

```python
class CapstoneState(TypedDict):
    request_id: str
    evidence: list[Document]
    attempts: int
    cost: float
    status: str
```

Expected output:

```text
A state record sufficient to explain every route and final outcome.
```

### Visual description

A state-machine diagram labels branches, limits, retries, and terminal states.

### Instructor notes

Require explicit non-success endings rather than converting every failure into prose.

### Notebook connection

The LangGraph quickstart provides the graph-building mechanics.

### Sources

- [LangGraph: Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangGraph: Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)

---

## Slide 7 - The API Contract Includes Failure Responses

### Teaching purpose

Connect workflow outcomes to a deployable interface.

### Learner-facing content

Define:

- request schema;
- response schema;
- authentication;
- authorization;
- status codes;
- idempotency where actions occur;
- request-size and rate limits;
- health checks;
- model and corpus versions.

Clients must distinguish supported answer, insufficient evidence, denied access, invalid input, and unavailable service.

### Worked example

`200` supported answer  
`200` typed insufficient-evidence response when the request is valid but evidence is absent  
`403` denied authorization  
`422` invalid request  
`503` provider unavailable

The contract documents which body accompanies each status.

### Code example

```python
@app.post("/answer", response_model=AnswerResponse)
def answer(request: AnswerRequest, user=Depends(authenticate)):
    return workflow.invoke(to_state(request, user))
```

Expected output:

```text
A typed API response derived from the workflow's final state.
```

### Visual description

One endpoint branches into documented success, insufficient, denied, invalid, and unavailable responses.

### Instructor notes

Ensure health checks do not call expensive model paths on every probe.

### Notebook connection

Week 11 deployment patterns wrap the final workflow.

### Sources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI: Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)

---

## Slide 8 - Evaluation Covers Components and User Outcomes

### Teaching purpose

Define a release evaluation plan.

### Learner-facing content

Evaluate:

- request validation;
- retrieval precision and recall;
- groundedness and citation support;
- structured-output validity;
- tool selection and arguments;
- workflow path and stopping;
- latency and cost;
- security and access isolation;
- user task success.

Use a versioned dataset containing normal, difficult, unsupported, denied, and failure cases.

### Worked example

Release thresholds:

- schema validity `100%`;
- citation IDs valid `100%`;
- groundedness at least `95%`;
- cross-tenant retrieval failures `0`;
- p95 latency under `3s`;
- p95 cost under `$0.02`.

### Code example

```python
release_ok = all(check.passed for check in evaluation_report.checks)
```

Expected output:

```text
True only when every required component and end-to-end check passes.
```

### Visual description

An evaluation matrix maps components to datasets, metrics, thresholds, and owners.

### Instructor notes

Require failed examples and not only aggregate scores.

### Notebook connection

Week 16's evaluation harness becomes the capstone release gate.

### Sources

- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [LangSmith: Evaluate RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)

---

## Slide 9 - Observability Connects a Result to Its Causes

### Teaching purpose

Define the production trace and monitoring signals.

### Learner-facing content

For each request, record:

- request and trace ID;
- code, model, prompt, schema, and corpus versions;
- graph path and node timings;
- retrieved chunk IDs and ranks;
- tool calls and outcomes;
- validation results;
- input/output tokens and cost;
- final status and error category.

Monitor availability, latency, errors, cost, retrieval drift, and delayed model-quality signals.

### Worked example

Latency trace:

validation `5ms`  
retrieval `120ms`  
generation `1,600ms`  
verification `80ms`

Total `1,805ms`; generation owns most latency.

### Code example

```python
trace.set_attributes({
    "model_version": MODEL_VERSION,
    "corpus_version": CORPUS_VERSION,
    "final_status": state["status"],
})
```

Expected output:

```text
A trace that can reproduce the component path behind one result.
```

### Visual description

A trace waterfall links versions, evidence, tools, validation, result, and monitoring dashboards.

### Instructor notes

Define redaction and retention before logging prompts or document content.

### Notebook connection

Tracing from Week 14 covers every graph node and external call.

### Sources

- [LangSmith: Observability](https://docs.langchain.com/langsmith/observability)
- [OpenTelemetry Concepts](https://opentelemetry.io/docs/concepts/)

---

## Slide 10 - Security and Cost Are Release Requirements

### Teaching purpose

Combine threat controls and resource budgets.

### Learner-facing content

Security controls:

- scoped identities and secrets;
- tenant-aware retrieval;
- input and output validation;
- tool allowlists and argument checks;
- human approval for high impact;
- dependency scanning;
- patching and rollback;
- log redaction.

Cost controls:

- token and tool-call budgets;
- rate limits;
- smallest suitable infrastructure;
- budget alerts;
- resource tags and cleanup;
- per-request and daily caps.

### Worked example

Attack: document contains tool instructions requesting data export.

Controls:

- retrieved text remains untrusted;
- export tool absent from allowlist;
- model has no credentials;
- authorization denies cross-tenant data;
- trace records denial.

### Code example

```python
if proposed_tool not in allowed_tools:
    return {"status": "denied", "reason": "tool_not_allowed"}
```

Expected output:

```text
A typed denial with no side effect and an auditable reason.
```

### Visual description

Threats meet preventive, detective, and response controls beside cost budget gates.

### Instructor notes

Require demonstration of one real blocked path and one budget-exhausted path.

### Notebook connection

The capstone integrates Week 11 deployment controls and Week 17 agent limits.

### Sources

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [AWS: Control Your Costs](https://docs.aws.amazon.com/hands-on/latest/control-your-costs-free-tier-budgets/control-your-costs-free-tier-budgets.html)

---

## Slide 11 - Release Includes Rollback and Failure Demonstrations

### Teaching purpose

Define production readiness beyond a successful demo.

### Learner-facing content

Before release, demonstrate:

- malformed request;
- unsupported question;
- unauthorized access;
- prompt injection;
- provider timeout;
- invalid model output;
- tool denial;
- budget exhaustion;
- health-check failure;
- rollback to previous artifact.

Create a runbook describing alerts, diagnosis, mitigation, rollback, owners, and cleanup.

### Worked example

New corpus index reduces groundedness below threshold.

Rollback:

1. stop routing to new index version;
2. restore previous version alias;
3. verify health and test cases;
4. record incident and failed changes;
5. correct ingestion before another release.

### Code example

```text
active_index -> policy-v3
candidate_index -> policy-v4
rollback changes active alias back to policy-v3
```

Expected output:

```text
The previous verified artifact serves requests without rebuilding during the incident.
```

### Visual description

A release pipeline points to versioned artifacts, canary checks, and a rollback arrow to the prior version.

### Instructor notes

Require rollback evidence, not only a written claim that rollback is possible.

### Notebook connection

The final notebook workflow is packaged with versioned model, corpus, prompt, and graph artifacts.

### Sources

- [AWS Well-Architected: Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Slide 12 - Capstone Deliverable: Evidence before Presentation

### Teaching purpose

Define the final assessment package and demonstration order.

### Learner-facing content

Submit:

1. problem statement and acceptance criteria;
2. architecture and data-flow diagrams;
3. threat model and cost estimate;
4. versioned source, configuration, and environment;
5. model and retrieval selection report;
6. API and workflow contracts;
7. evaluation dataset and results;
8. failure-analysis report;
9. deployment and health evidence;
10. traces, monitoring, and budget alerts;
11. runbook and rollback proof;
12. limitations and responsible-use statement.

Demonstrate failure paths before the polished success path.

### Worked example

Final demonstration:

1. denied cross-tenant request;
2. unsupported question;
3. malformed output caught by validation;
4. provider timeout and controlled response;
5. grounded answer with verified citations;
6. rollback to previous artifact.

### Code example

```python
assert release_report.all_required_checks_pass
assert release_report.rollback_verified
```

Expected output:

```text
Both assertions pass before the capstone is marked production-ready.
```

### Visual description

A final evidence board connects requirements to implementation, tests, deployment, operations, rollback, and presentation.

### Instructor notes

Grade the evidence chain and failure handling more heavily than interface polish.

### Notebook connection

Use one selected agentic capstone notebook as a starting pattern and document every modernization or replacement.

### Sources

- [AI Bootcamp Repository](https://github.com/curiousily/AI-Bootcamp)
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
