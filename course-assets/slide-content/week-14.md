# Week 14: Engineering LLM Applications

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who can make a validated model call and define read-only tools  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 14 presentation and related media.

---

## Slide 1 - An LLM Application Is More Than a Model Call

### Teaching purpose

Define application-owned layers around the provider.

### Learner-facing content

An engineered LLM application includes:

- request validation;
- prompt and schema versioning;
- provider client;
- model selection;
- retries and timeouts;
- structured-output validation;
- tool authorization;
- tracing and metrics;
- fallback and failure behaviour;
- cost and token controls.

The application owns reliability and security. A provider response is untrusted input until validated.

### Worked example

User request flows through:

`API -> validation -> prompt -> provider -> schema check -> policy check -> response`

If schema validation fails, the application returns a controlled error or bounded retry rather than storing malformed data.

### Code example

```python
request = RequestModel.model_validate(payload)
raw = llm_client.generate(build_messages(request))
result = ResponseModel.model_validate(raw)
```

Expected output:

```text
A typed response or a controlled validation failure.
```

### Visual description

The model provider is one box inside a larger application boundary with validation, policy, observability, and cost controls.

### Instructor notes

Ask which responsibilities remain even when the provider advertises structured output.

### Notebook connection

The LiteLLM and LangChain notebooks expose provider calls that this week wraps in application contracts.

### Sources

- [AI Bootcamp: Multiple LLM Providers with LiteLLM](https://github.com/curiousily/AI-Bootcamp/blob/master/26.multiple-llm-providers-with-litellm.ipynb)
- [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)

---

## Slide 2 - Authentication Proves Which Application Is Calling

### Teaching purpose

Teach API-key handling and scoped identity.

### Learner-facing content

Provider APIs require **authentication**, often through an API key or cloud identity.

Rules:

- keep credentials outside source code and notebooks;
- use environment variables or a secret manager;
- separate development and production credentials;
- grant minimum required permissions and spend limits;
- rotate exposed keys;
- never log authorization headers;
- fail clearly when configuration is missing.

Authentication identifies a caller. **Authorization** decides what that caller may do.

### Worked example

Unsafe notebook:

`api_key = "live-key-value"`

Safer application:

`api_key = os.environ["PROVIDER_API_KEY"]`

The deployment environment injects the secret; the repository never stores it.

### Code example

```python
import os

api_key = os.environ["PROVIDER_API_KEY"]
client = ProviderClient(api_key=api_key)
```

Expected output:

```text
An authenticated client or a clear startup error when the secret is absent.
```

### Visual description

A secret manager injects a scoped key into runtime memory; repository, logs, and image layers remain key-free.

### Instructor notes

Remind learners that the root `.env` is local sensitive material and must remain ignored.

### Notebook connection

Provider notebooks should read keys from environment variables, never checked-in cells.

### Sources

- [OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [AWS: Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)

---

## Slide 3 - Model Selection Starts with Required Capabilities

### Teaching purpose

Replace “best model” thinking with task requirements and measured tradeoffs.

### Learner-facing content

Select a model using:

- task quality on your evaluation set;
- required context length;
- structured-output and tool support;
- latency;
- input and output price;
- data location and retention terms;
- rate limits;
- language and modality support;
- deployment constraints.

Model names and capabilities change. Pin a model identifier where supported and record the observed version.

### Worked example

Task requires JSON extraction under `2` seconds.

Model A: 98% field accuracy, 4 seconds.  
Model B: 96% field accuracy, 1 second.  
Model C: 90% field accuracy, 0.5 seconds.

Selection depends on the minimum accepted quality and latency requirement.

### Code example

```python
requirements = {
    "structured_output": True,
    "p95_latency_ms": 2000,
    "field_accuracy_min": 0.95,
}
```

Expected output:

```text
A capability and acceptance contract used to compare candidate models.
```

### Visual description

A requirements table filters candidate models, then an evaluation set compares survivors.

### Instructor notes

Do not make current vendor recommendations in the slides; learners must evaluate currently available models.

### Notebook connection

The LiteLLM notebook sends the same task to several providers for controlled comparison.

### Sources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LangSmith: Evaluation](https://docs.langchain.com/langsmith/evaluation)

---

## Slide 4 - Streaming Delivers Partial Output Events

### Teaching purpose

Explain streaming, buffering, cancellation, and structured-output limits.

### Learner-facing content

**Streaming** returns partial events while generation continues.

Benefits:

- faster time to first visible token;
- progressive user feedback;
- ability to cancel long generations.

Engineering requirements:

- assemble chunks in order;
- handle disconnects and cancellation;
- avoid treating partial JSON as valid;
- record complete and failed streams;
- apply final validation after completion.

Streaming improves perceived latency, not total generation work.

### Worked example

Chunks:

`"The "` -> `"answer "` -> `"is 42."`

The interface can display text progressively. For JSON, buffer until the complete object arrives, then parse and validate.

### Code example

```python
parts = []
for event in client.stream(messages):
    parts.append(event.text)
complete_text = "".join(parts)
```

Expected output:

```text
One ordered final string assembled from provider events.
```

### Visual description

A timeline shows request, first token, progressive chunks, complete response, and final validation.

### Instructor notes

Explain that users must be warned or protected from acting on incomplete unvalidated output.

### Notebook connection

Learners add streaming to one provider call and measure time to first token and total time.

### Sources

- [LiteLLM: Streaming](https://docs.litellm.ai/docs/completion/stream)
- [LangChain: Streaming](https://docs.langchain.com/oss/python/langchain/streaming)

---

## Slide 5 - Tokens Drive Context, Latency, and Cost

### Teaching purpose

Teach per-request budgets and observable token use.

### Learner-facing content

Provider usage commonly separates:

- input tokens;
- output tokens;
- sometimes cached or reasoning tokens.

Approximate request cost:

`input_tokens x input_rate + output_tokens x output_rate`

Rates must use the provider's current units, often price per million tokens.

Set limits on input size, retrieved context, output length, total request cost, and daily spend.

### Worked example

Input `2,000` tokens at `$1` per million:

`2000 / 1,000,000 x $1 = $0.002`

Output `500` tokens at `$4` per million:

`500 / 1,000,000 x $4 = $0.002`

Estimated total `$0.004`.

### Code example

```python
estimated = input_tokens / 1_000_000 * input_rate
estimated += output_tokens / 1_000_000 * output_rate
```

Expected output:

```text
A per-request estimate using current provider rates and observed token counts.
```

### Visual description

A context budget and cost equation connect input, output, limits, and daily aggregate.

### Instructor notes

Label prices as examples only. Never hardcode slides as a current pricing source.

### Notebook connection

The lab logs token counts, latency, and estimated cost for each provider.

### Sources

- [LiteLLM: Cost Tracking](https://docs.litellm.ai/docs/completion/token_usage)
- [Hugging Face: Generation Parameters](https://huggingface.co/docs/transformers/main_classes/text_generation)

---

## Slide 6 - Retries Handle Transient Failures, Not Every Failure

### Teaching purpose

Teach bounded retries, backoff, jitter, timeout, and idempotency.

### Learner-facing content

Retry only failures likely to be temporary, such as some timeouts, connection failures, `429` rate limits, or provider `5xx` responses.

Do not retry invalid credentials, malformed requests, or permanent policy failures.

Use:

- per-attempt timeout;
- maximum attempts;
- exponential backoff;
- random jitter;
- total time budget;
- idempotency protections for actions.

### Worked example

Backoff base `1` second:

attempt delays approximately `1`, `2`, and `4` seconds, plus jitter.

With a three-attempt cap and ten-second total budget, the request cannot retry forever.

### Code example

```python
for attempt in range(3):
    try:
        return call_provider(timeout=10)
    except TransientError:
        sleep(2**attempt + random.random())
raise ProviderUnavailable()
```

Expected output:

```text
Success within the retry budget or one controlled unavailable error.
```

### Visual description

Transient errors enter a bounded backoff loop; permanent errors exit immediately.

### Instructor notes

Explain duplicate side effects: retrying a generation is different from retrying “send email.”

### Notebook connection

The provider wrapper adds bounded retries around transient failures.

### Sources

- [AWS: Retry with Backoff Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html)
- [LiteLLM: Reliability](https://docs.litellm.ai/docs/proxy/reliability)

---

## Slide 7 - A Provider Adapter Normalizes What Can Be Normalized

### Teaching purpose

Explain the value and limits of LiteLLM.

### Learner-facing content

A **provider adapter** gives application code one interface for several providers.

LiteLLM can normalize common request and response shapes, token usage, exceptions, routing, and fallbacks.

Capabilities still differ:

- tool and schema formats;
- supported parameters;
- context limits;
- multimodal input;
- safety behaviour;
- streaming events.

The application should check required capabilities instead of assuming every provider behaves identically.

### Worked example

Application call:

`complete(model_alias, messages, schema)`

Configuration maps `model_alias` to Provider A or B. If Provider B lacks strict schema support, the capability check blocks that route rather than silently weakening validation.

### Code example

```python
from litellm import completion

response = completion(model=model_id, messages=messages)
```

Expected output:

```text
A normalized completion response containing provider-specific metadata when available.
```

### Visual description

One application interface fans out to three providers; capability gates sit before each route.

### Instructor notes

Explain abstraction leakage: normalized syntax does not mean identical semantics.

### Notebook connection

The LiteLLM notebook compares text, structured output, and tool calls across providers.

### Sources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [AI Bootcamp: Multiple LLM Providers with LiteLLM](https://github.com/curiousily/AI-Bootcamp/blob/master/26.multiple-llm-providers-with-litellm.ipynb)

---

## Slide 8 - LangChain Composes Models, Prompts, Parsers, and Tools

### Teaching purpose

Introduce framework components after the underlying concepts.

### Learner-facing content

LangChain provides interfaces and composition tools for:

- chat models;
- prompt templates;
- structured output;
- retrieval;
- tools;
- streaming;
- tracing.

A framework reduces integration code but does not remove the need to understand message roles, schema validation, retries, permissions, or evaluation.

Prefer small explicit chains whose inputs and outputs are typed and observable.

### Worked example

Chain:

`validated request -> prompt template -> chat model -> structured output model`

The chain's input is a topic string. Its output is a validated `Summary` object, not unparsed prose.

### Code example

```python
structured_model = model.with_structured_output(Summary)
chain = prompt | structured_model
result = chain.invoke({"document": document})
```

Expected output:

```text
A validated Summary object when the provider and schema contract succeed.
```

### Visual description

Four explicit components connect with typed arrows and visible trace boundaries.

### Instructor notes

Expand the chain into its underlying model call and parser so learners know what the operator hides.

### Notebook connection

The LangChain foundations notebook covers model calls, structured output, PDFs, tools, and tracing.

### Sources

- [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [AI Bootcamp: LangChain Foundations](https://github.com/curiousily/AI-Bootcamp/blob/master/27.langchain-foundations.ipynb)

---

## Slide 9 - Tracing Records Every Important Boundary

### Teaching purpose

Define traces, spans, and the minimum LLM request record.

### Learner-facing content

A **trace** records one end-to-end application request. A **span** records one operation inside it.

Capture:

- trace and request ID;
- prompt and schema version;
- provider and model;
- token usage and latency;
- retry count;
- tool proposals and results;
- validation outcomes;
- final status and error category;
- cost estimate.

Protect personal data and secrets through redaction and retention rules.

### Worked example

One request trace contains:

`validate 3ms -> retrieve 80ms -> model 1200ms -> parse 4ms`

Total observed span time is approximately `1,287ms`, revealing that the model call dominates latency.

### Code example

```python
with tracer.start_as_current_span("llm_request") as span:
    span.set_attribute("model", model_id)
    result = call_model()
```

Expected output:

```text
One searchable trace connecting request metadata and nested operation timings.
```

### Visual description

A waterfall trace shows validation, retrieval, model, parser, and tool spans on one timeline.

### Instructor notes

Explain that logging full prompts can create privacy and security risk; capture only what policy allows.

### Notebook connection

Learners enable tracing around the LangChain and LiteLLM calls.

### Sources

- [LangSmith: Observability](https://docs.langchain.com/langsmith/observability)
- [LangSmith: Trace LiteLLM](https://docs.langchain.com/langsmith/trace-litellm)

---

## Slide 10 - MCP Standardizes Tools and Resources

### Teaching purpose

Introduce Model Context Protocol roles and boundaries.

### Learner-facing content

The **Model Context Protocol (MCP)** standardizes how an application connects to servers that expose:

- **tools:** bounded operations the client may request;
- **resources:** readable context with stable identifiers;
- **prompts:** reusable prompt templates where supported.

An MCP client discovers capabilities and sends requests. The server still enforces authentication, authorization, input validation, path boundaries, timeouts, and output limits.

MCP does not make every connected capability safe to expose.

### Worked example

Filesystem MCP server:

- resource: approved course handout;
- tool: search within approved course directory;
- forbidden: read arbitrary paths or write files.

The server resolves and checks paths before access.

### Code example

```text
Client -> list tools -> call read_course_file(path)
Server -> validate root and size -> return content or denied error
```

Expected output:

```text
A bounded resource result whose origin and permission checks are explicit.
```

### Visual description

Host application and model connect through an MCP client to scoped servers; trust boundaries and permission gates are labelled.

### Instructor notes

Separate protocol interoperability from security policy. Use least privilege per server.

### Notebook connection

MCP is introduced conceptually before agent workflows use external tools.

### Sources

- [Model Context Protocol: Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Model Context Protocol: Architecture](https://modelcontextprotocol.io/docs/learn/architecture)

---

## Slide 11 - Resilience Needs Explicit Fallback Behaviour

### Teaching purpose

Combine limits, provider failure, fallback, and user-visible degradation.

### Learner-facing content

A resilient request path defines:

- validation failure;
- context-too-large handling;
- rate-limit and timeout behaviour;
- schema failure;
- provider outage;
- tool denial or timeout;
- fallback eligibility;
- user-visible error;
- trace and alert.

A fallback model is acceptable only if it supports required capabilities and passes the task's quality threshold. Silent fallback can change output quality, data location, or cost.

### Worked example

Primary provider times out twice.

If the request requires strict JSON and approved fallback supports it, route once to fallback and record the change. Otherwise return a controlled unavailable error.

### Code example

```python
if primary_failed and fallback.supports(required_capabilities):
    return fallback.generate(request)
raise ServiceUnavailable()
```

Expected output:

```text
One explicit fallback result or a bounded unavailable response.
```

### Visual description

Primary and fallback paths share capability, policy, validation, and observability gates.

### Instructor notes

Ask what changes when data is sent to another provider. Require policy approval, not just technical availability.

### Notebook connection

The LiteLLM lab tests one simulated timeout and one capability-incompatible fallback.

### Sources

- [LiteLLM: Reliability](https://docs.litellm.ai/docs/proxy/reliability)
- [LangSmith: Observability](https://docs.langchain.com/langsmith/observability)

---

## Slide 12 - Guided Lab: Build a Provider-Resilient Service

### Teaching purpose

Set the Week 14 application-engineering deliverable.

### Learner-facing content

Build a small extraction API that:

1. validates request input;
2. reads credentials from environment;
3. supports two provider configurations;
4. checks structured-output capability;
5. streams text only where partial output is safe;
6. limits input and output tokens;
7. records token use, latency, and estimated cost;
8. retries only transient failures;
9. validates every final object;
10. traces model and tool spans;
11. exposes one read-only tool or MCP resource;
12. demonstrates fallback and controlled failure.

### Worked example

Test matrix:

- valid request;
- invalid schema;
- provider timeout;
- rate limit;
- unsupported capability;
- tool permission denial;
- output over budget.

Each case has an expected status and trace.

### Code example

```python
result = service.extract(request)
assert isinstance(result, ExtractedRecord)
assert trace.token_usage <= request.token_budget
```

Expected output:

```text
A validated result within budget, or a typed controlled failure.
```

### Visual description

An end-to-end service diagram labels API, provider adapter, validation, tracing, tool/MCP, fallback, and cost controls.

### Instructor notes

Require failure demonstrations, not only a successful provider call.

### Notebook connection

Complete `26.multiple-llm-providers-with-litellm.ipynb` and `27.langchain-foundations.ipynb`.

### Sources

- [AI Bootcamp: Multiple LLM Providers with LiteLLM](https://github.com/curiousily/AI-Bootcamp/blob/master/26.multiple-llm-providers-with-litellm.ipynb)
- [AI Bootcamp: LangChain Foundations](https://github.com/curiousily/AI-Bootcamp/blob/master/27.langchain-foundations.ipynb)
