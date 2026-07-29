# Week 11: Serving and Deploying Models

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners with a tested and serialized machine-learning pipeline  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 11 presentation and related media.

---

## Slide 1 - Serving Turns a Fitted Model into a Service

### Teaching purpose

Define inference service boundaries before cloud tools.

### Learner-facing content

**Model serving** makes a fitted model available to another program.

A serving request contains feature values. The service:

1. validates the request;
2. applies the saved preprocessing pipeline;
3. calculates inference;
4. formats a response;
5. records operational evidence.

Training and serving must use the same feature definitions and fitted artifact. A successful HTTP response does not prove the prediction is correct.

### Worked example

Request: `{"age": 35, "city": "Kandy"}`

The service validates types, applies the saved imputer and encoder, returns a probability and model version, then logs latency without exposing secrets.

### Code example

```python
features = {"age": 35, "city": "Kandy"}
prediction = pipeline.predict_proba([features])[0, 1]
print(prediction)
```

Expected output:

```text
A positive-class probability produced by the saved pipeline.
```

### Visual description

Client, validation, preprocessing, model, response, and logging form a left-to-right request path.

### Instructor notes

Separate training jobs from online inference. Re-emphasize that the persisted artifact includes preprocessing.

### Notebook connection

This week wraps the Week 10 pipeline in an API rather than retraining it inside each request.

### Sources

- [Scikit-learn: Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

## Slide 2 - HTTP Defines Requests and Responses

### Teaching purpose

Teach the protocol vocabulary needed to use an API.

### Learner-facing content

**HTTP** is a protocol for exchanging requests and responses.

A request contains:

- method such as `GET` or `POST`;
- path such as `/predict`;
- headers such as content type or authorization;
- optional body containing input data.

A response contains a status code, headers, and optional body.

Common codes:

- `200`: success
- `400` or `422`: invalid client input
- `401` or `403`: authentication or permission failure
- `500`: unexpected server failure

### Worked example

`POST /predict` sends feature JSON because prediction creates a computation from a structured body.

Valid input returns `200`. Missing required age returns a validation error, commonly `422` in FastAPI.

### Code example

```text
POST /predict HTTP/1.1
Content-Type: application/json

{"age": 35, "city": "Kandy"}
```

Expected output:

```text
HTTP 200 with a structured JSON prediction response.
```

### Visual description

A request envelope and response envelope label method, path, headers, body, status, and response body.

### Instructor notes

Explain that HTTP status and model result are different: a valid negative prediction still returns success.

### Notebook connection

Learners will send test requests to the local FastAPI application.

### Sources

- [MDN: Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [FastAPI: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

---

## Slide 3 - JSON and Validation Define the API Contract

### Teaching purpose

Show how typed input blocks malformed inference requests.

### Learner-facing content

**JSON** represents objects, arrays, strings, numbers, booleans, and null.

An **API contract** states required fields, data types, ranges, response fields, and error behaviour.

Validation should reject:

- missing required fields;
- wrong types;
- values outside valid ranges;
- unknown fields when strict input is required;
- requests that exceed size limits.

Validation protects the service boundary; it does not replace data-drift monitoring.

### Worked example

Contract:

- `age`: integer from `18` to `100`
- `city`: non-empty string

`{"age": "thirty-five"}` fails type and missing-city checks before model inference.

### Code example

```python
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    city: str = Field(min_length=1)
```

Expected output:

```text
Valid JSON becomes a typed request object; invalid JSON returns field-level errors.
```

### Visual description

Valid and invalid JSON documents pass through a schema gate; only the valid request reaches the model.

### Instructor notes

Ask which training schema assumptions can be enforced at the API boundary.

### Notebook connection

The request schema must match the columns expected by the persisted pipeline.

### Sources

- [FastAPI: Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic: Fields](https://docs.pydantic.dev/latest/concepts/fields/)

---

## Slide 4 - FastAPI Connects a Typed Contract to Inference

### Teaching purpose

Build a minimal endpoint learners can explain line by line.

### Learner-facing content

**FastAPI** maps HTTP paths and methods to Python functions.

The endpoint should:

1. accept a typed request;
2. convert it into the model's row format;
3. call the loaded pipeline;
4. return JSON-safe values;
5. convert expected failures into clear client errors.

Load the model once when the application starts, not once per request.

### Worked example

For probability `0.73` and threshold `0.50`, return:

```json
{"label": 1, "probability": 0.73, "model_version": "2026-07-28"}
```

The version lets logs and clients identify the producing artifact.

### Code example

```python
@app.post("/predict")
def predict(request: PredictionRequest):
    row = pd.DataFrame([request.model_dump()])
    probability = float(model.predict_proba(row)[0, 1])
    return {"label": int(probability >= 0.5), "probability": probability}
```

Expected output:

```text
A validated JSON response containing a class label and probability.
```

### Visual description

Route decorator, request model, DataFrame row, pipeline, and response fields are linked to code lines.

### Instructor notes

Explain every conversion. Avoid hiding schema mismatches in broad exception handlers.

### Notebook connection

The lab uses the complete saved pipeline and a small local API test.

### Sources

- [FastAPI: Path Operation Decorators](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)
- [FastAPI: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)

---

## Slide 5 - Health Checks Separate Availability from Prediction Quality

### Teaching purpose

Define startup, liveness, and readiness evidence.

### Learner-facing content

A **health check** is a lightweight endpoint used by operators or infrastructure.

- **Liveness:** is the process running?
- **Readiness:** can it currently serve valid requests?
- **Startup:** has initialization completed?

A readiness check may confirm the model loaded and required dependencies are available. It should not perform an expensive full prediction on every probe.

Health checks do not measure model accuracy or data drift.

### Worked example

`GET /health/ready`

Ready response:

```json
{"status": "ready", "model_version": "2026-07-28"}
```

If the model failed to load, return a non-success status so traffic is not routed to the process.

### Code example

```python
@app.get("/health/ready")
def ready():
    return {"status": "ready", "model_version": MODEL_VERSION}
```

Expected output:

```text
HTTP 200 only after the application artifact is ready for inference.
```

### Visual description

Liveness, readiness, and model-quality checks appear as separate gauges with different consumers.

### Instructor notes

Ask what would make the process alive but not ready.

### Notebook connection

The deployment lab verifies health before sending prediction traffic.

### Sources

- [Kubernetes: Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [FastAPI: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)

---

## Slide 6 - Docker Packages the Application Environment

### Teaching purpose

Define images and containers without conflating them with virtual machines.

### Learner-facing content

A Docker **image** is an immutable filesystem and configuration template. A **container** is a running process created from an image.

A model API image should include:

- application code;
- pinned dependencies;
- trusted model artifact;
- startup command;
- non-secret defaults.

Build once and run the same image in test and production. Use a small trusted base image, a non-root user, and explicit version tags or digests.

### Worked example

Build:

`docker build -t dsacademy-model:1.0 .`

Run:

`docker run -p 8000:8000 dsacademy-model:1.0`

The host port `8000` forwards to the container service port.

### Code example

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["fastapi", "run", "app.py", "--port", "8000"]
```

Expected output:

```text
One reproducible image that starts the API on port 8000.
```

### Visual description

A Dockerfile builds an image; the image starts identical containers in local and EC2 environments.

### Instructor notes

Explain that data and secrets should not be baked into public image layers.

### Notebook connection

The lab containerizes the API only after local validation passes.

### Sources

- [FastAPI: Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker: Images and Containers](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)

---

## Slide 7 - Configuration and Secrets Belong Outside Source Code

### Teaching purpose

Teach environment variables and least-privilege secret handling.

### Learner-facing content

**Configuration** changes application behaviour between environments. A **secret** grants access, such as an API key or password.

Environment variables can supply configuration at runtime:

`MODEL_PATH`, `LOG_LEVEL`, `PREDICTION_THRESHOLD`

Do not commit `.env` files containing real credentials. In production, use a managed secret store or scoped instance role. Rotate exposed credentials and avoid printing them in logs.

### Worked example

Unsafe:

```python
AWS_SECRET = "actual-secret"
```

Safer runtime lookup:

```python
threshold = float(os.environ["PREDICTION_THRESHOLD"])
```

The application fails clearly if required configuration is missing.

### Code example

```python
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "/app/model.joblib")
```

Expected output:

```text
The runtime value is used when set; otherwise the non-secret default path is used.
```

### Visual description

Source code and container image remain unchanged while local, test, and production environments inject different configuration.

### Instructor notes

Distinguish a convenient local `.env` file from a production secret-management system.

### Notebook connection

The deployment exercise keeps environment-specific values outside the application module.

### Sources

- [Docker: Environment Variables](https://docs.docker.com/compose/how-tos/environment-variables/)
- [AWS: Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)

---

## Slide 8 - EC2 Is a Virtual Server You Must Operate

### Teaching purpose

Explain the minimum AWS components and operational responsibility.

### Learner-facing content

An Amazon EC2 **instance** is a virtual server.

Key components:

- AMI: operating-system image;
- instance type: CPU and memory capacity;
- EBS volume: persistent block storage;
- VPC and subnet: network placement;
- security group: allowed network traffic;
- key pair or managed access method;
- IAM role: scoped AWS permissions.

A low-cost instance can run for months, but you remain responsible for patches, availability, backups, security, monitoring, and charges while it runs.

### Worked example

For a small CPU-only API, choose the smallest architecture-compatible instance that meets measured memory needs. Start with one instance, no load balancer, and a documented restart procedure.

### Code example

```text
AMI -> EC2 instance -> Docker container -> FastAPI -> model pipeline
```

Expected output:

```text
One reachable inference service with an explicit artifact and network path.
```

### Visual description

An EC2 instance boundary contains Docker, FastAPI, and the model; VPC, EBS, IAM, and security group surround it.

### Instructor notes

Explain that “cheap” is not the same as free and Free Tier eligibility depends on account terms and current usage.

### Notebook connection

The lab can deploy to EC2 after local Docker verification; no GPU is required for the small model.

### Sources

- [AWS: Get Started with EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [AWS: What Is EC2?](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)

---

## Slide 9 - Security Groups Expose Only Required Traffic

### Teaching purpose

Teach network rules and safe remote access.

### Learner-facing content

An EC2 **security group** is a stateful virtual firewall.

Inbound rules should allow only required ports and sources:

- SSH `22`: restrict to an administrator IP, or avoid public SSH by using managed access;
- HTTP `80`: redirect to HTTPS when used;
- HTTPS `443`: public only when the API is intended to be public;
- application port `8000`: keep private behind a reverse proxy when possible.

Never expose every port to `0.0.0.0/0`.

### Worked example

Safer rules:

- `443` from intended clients;
- `22` from one administrator CIDR;
- no public rule for `8000`.

The reverse proxy terminates TLS and forwards internally to FastAPI.

### Code example

```text
Internet :443 -> reverse proxy -> localhost:8000 -> FastAPI
Admin IP :22 -> EC2
```

Expected output:

```text
Only encrypted client traffic and restricted administration reach the instance.
```

### Visual description

Allowed arrows pass through a security-group boundary; broad SSH and direct app-port arrows are blocked.

### Instructor notes

Explain CIDR at a high level and warn against temporary broad rules left in place.

### Notebook connection

The deployment checklist records every open port, protocol, source, and reason.

### Sources

- [AWS: EC2 Security Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
- [AWS: Create a Security Group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-security-group.html)

---

## Slide 10 - Logs and Metrics Make Failures Observable

### Teaching purpose

Define operational evidence without logging sensitive payloads.

### Learner-facing content

**Logs** record discrete events. **Metrics** summarize numerical behaviour over time.

Record:

- timestamp and request ID;
- model version;
- status code and error type;
- latency;
- request and prediction counts;
- resource use;
- input-schema failures;
- carefully designed drift indicators.

Do not log secrets or unnecessary personal data. Prediction quality often arrives later, when actual outcomes become available.

### Worked example

From `1,000` requests:

- `990` successful;
- `8` validation failures;
- `2` server failures.

Server error rate:

`2 / 1000 = 0.002 = 0.2%`

### Code example

```python
logger.info(
    "prediction_complete",
    extra={"request_id": request_id, "latency_ms": 42, "model_version": MODEL_VERSION},
)
```

Expected output:

```text
A structured event that can be searched and aggregated without exposing features.
```

### Visual description

Requests generate structured logs, metrics, dashboard panels, and an alert when an explicit threshold is crossed.

### Instructor notes

Separate application health, data drift, and model quality; they use different evidence.

### Notebook connection

The lab verifies logs for success, validation failure, and unexpected failure.

### Sources

- [AWS CloudWatch: Getting Started](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GettingStarted.html)
- [OpenTelemetry: Logs, Metrics, and Traces](https://opentelemetry.io/docs/concepts/signals/)

---

## Slide 11 - Cost Controls Start Before the Instance

### Teaching purpose

Make low-cost deployment measurable and bounded.

### Learner-facing content

Cloud costs continue while resources run.

Before deployment:

- confirm current Free Tier or credit eligibility;
- estimate instance and storage cost;
- choose the smallest measured capacity;
- set AWS Budgets alerts;
- tag resources with owner and purpose;
- define stop or termination dates;
- remove unused snapshots, IPs, and volumes;
- avoid optional paid services unless justified.

Stopping an instance may leave EBS storage billed. Termination and deletion policies must be deliberate.

### Worked example

Monthly estimate:

`hourly rate x 24 x 30 + storage + data transfer`

Even when compute is covered by credits, storage or transfer may not be. The exact rate must be checked for region, account, and date.

### Code example

```text
Budget alert: 50% -> review
Budget alert: 80% -> stop nonessential service
Budget alert: 100% -> terminate lab resources
```

Expected output:

```text
A documented response before spending exceeds the agreed limit.
```

### Visual description

A cost meter connects estimate, tags, budget alerts, stop date, and cleanup checklist.

### Instructor notes

Do not quote a fixed Free Tier allowance. AWS terms changed in 2025 and differ by account age and credits.

### Notebook connection

The deployment lab includes a resource inventory and cleanup verification.

### Sources

- [AWS: Control Your Costs](https://docs.aws.amazon.com/hands-on/latest/control-your-costs-free-tier-budgets/control-your-costs-free-tier-budgets.html)
- [AWS Free Tier](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html)

---

## Slide 12 - Guided Lab: Deploy, Verify, and Clean Up

### Teaching purpose

Set an end-to-end deployment exercise with security and cost evidence.

### Learner-facing content

Complete:

1. local API contract tests;
2. model loaded once at startup;
3. health and prediction endpoints;
4. Docker image build and local run;
5. environment-based configuration;
6. smallest suitable EC2 instance;
7. restricted security-group rules;
8. HTTPS or a clearly bounded private test;
9. success and failure logs;
10. budget alert and resource tags;
11. rollback procedure;
12. stop, terminate, or cleanup verification.

### Worked example

Verification sequence:

`GET /health/ready -> 200`  
valid `POST /predict -> 200`  
invalid input `-> 422`  
unknown path `-> 404`  
logs contain request IDs and no secrets.

### Code example

```bash
curl -sS https://example.test/health/ready
curl -sS -X POST https://example.test/predict \
  -H 'content-type: application/json' \
  -d '{"age":35,"city":"Kandy"}'
```

Expected output:

```text
A ready response followed by a typed prediction response.
```

### Visual description

A release checklist follows local test, image, EC2, network, health, prediction, logs, budget, rollback, and cleanup.

### Instructor notes

Use free-tier-eligible or credit-covered resources only when the account confirms eligibility. Terminate all lab resources after evidence is captured.

### Notebook connection

This deployment lab packages the Week 10 pipeline and prepares learners for model-backed AI services.

### Sources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [AWS: Get Started with EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
