"""Build substantive slide and narration outlines for DS Academy sessions."""

from __future__ import annotations


CONCEPT_DEFINITIONS = {
	"data types": "Data types define the values an operation can accept and the behavior that operation will produce.",
	"control flow": "Control flow decides which statements run, how often they run, and when execution stops.",
	"functions": "Functions package a named transformation behind explicit inputs, outputs, and side-effect boundaries.",
	"exceptions": "Exceptions make failure states visible so software can recover, report, or stop deliberately.",
	"ndarrays": "An ndarray stores homogeneous values in a fixed-dimensional structure optimized for numerical work.",
	"indexing": "Indexing selects scalar values, slices, masks, or coordinate ranges from an array.",
	"vectorization": "Vectorization expresses an operation over complete arrays so optimized kernels replace Python loops.",
	"broadcasting": "Broadcasting aligns compatible array shapes without materializing repeated data.",
	"Git history": "Git history is an auditable sequence of snapshots that records what changed and why.",
	"branching": "Branching isolates a line of work so it can be reviewed and integrated without destabilizing the main line.",
	"project layout": "Project layout assigns stable locations to source, tests, configuration, data, and generated artifacts.",
	"environments": "An environment pins the interpreter and dependencies required to reproduce an execution.",
	"HTTP": "HTTP defines how clients and servers exchange requests, responses, headers, status codes, and bodies.",
	"JSON": "JSON is a portable text representation for nested objects, arrays, numbers, strings, booleans, and null.",
	"API contracts": "An API contract specifies accepted inputs, returned outputs, error behavior, and compatibility expectations.",
	"application state": "Application state is the data a user interface or service must retain between interactions.",
	"data quality": "Data quality measures whether data is complete, valid, consistent, timely, and fit for its intended decision.",
	"missing values": "Missing values encode absent observations whose cause and handling can materially change an analysis.",
	"types": "Types constrain representation and operations, helping expose invalid values before downstream use.",
	"validation": "Validation checks data or model behavior against explicit rules before it crosses a trust boundary.",
	"distributions": "A distribution describes the frequency, center, spread, shape, and extremes of observed values.",
	"group comparisons": "Group comparisons reveal how outcomes and errors vary across meaningful segments.",
	"correlation": "Correlation summarizes association between variables but does not establish a causal mechanism.",
	"bias": "Bias is a systematic distortion introduced by data collection, assumptions, measurement, or modelling choices.",
	"encoding": "Encoding converts categories or structured values into numerical representations a model can consume.",
	"scaling": "Scaling changes numerical ranges while preserving an intended relationship between values.",
	"time features": "Time features represent calendar cycles, elapsed durations, recency, and event order without leaking the future.",
	"leakage": "Leakage occurs when training uses information that would not be available at prediction time.",
	"fit and transform": "Fit learns transformation parameters; transform applies those learned parameters to new data.",
	"ColumnTransformer": "ColumnTransformer applies different preprocessing branches to selected columns in one fitted object.",
	"Pipeline": "A Pipeline binds preprocessing and estimation into one ordered, testable training and inference contract.",
	"serialization": "Serialization stores a fitted artifact so it can be loaded and used with the same behavior later.",
	"baseline": "A baseline is a credible simple rule that establishes the minimum performance a model must beat.",
	"least squares": "Least squares estimates parameters by minimizing the sum of squared residuals.",
	"coefficients": "Coefficients quantify a model's fitted relationship between inputs and an output under its assumptions.",
	"residuals": "Residuals are the differences between observed and predicted values and expose missed structure.",
	"regularization": "Regularization penalizes complexity to improve stability and reduce sensitivity to noise.",
	"bias and variance": "Bias and variance describe underfitting from rigid assumptions and overfitting from unstable flexibility.",
	"trees": "Decision trees partition feature space with rules that create locally homogeneous predictions.",
	"cross-validation": "Cross-validation repeats training and validation across folds to estimate variation in performance.",
	"holdout": "A holdout set is reserved from fitting so it can provide an independent performance estimate.",
	"time splits": "Time splits train on earlier observations and validate on later ones to imitate temporal deployment.",
	"hyperparameters": "Hyperparameters control model structure or training behavior and must be selected inside validation boundaries.",
	"metric choice": "Metric choice translates the operational cost of errors into a measurable evaluation objective.",
	"confidence": "Confidence communicates uncertainty around an estimate instead of treating one observed score as exact.",
	"segments": "Segments are meaningful subsets used to find performance differences hidden by aggregate results.",
	"failure modes": "Failure modes are recurring conditions under which a system produces unsafe, invalid, or low-value outcomes.",
	"logistic regression": "Logistic regression maps a linear score to a probability for a binary outcome.",
	"probability": "Probability represents calibrated uncertainty about an outcome on a scale from zero to one.",
	"thresholds": "A threshold converts a probability into an action and encodes a tradeoff between error types.",
	"calibration": "Calibration checks whether predicted probabilities match observed event frequencies.",
	"decision trees": "Decision trees learn ordered feature rules that split observations into prediction regions.",
	"ensembles": "Ensembles combine multiple models to reduce variance, bias, or sensitivity to individual errors.",
	"class imbalance": "Class imbalance occurs when important outcomes are rare enough to distort training and evaluation.",
	"precision and recall": "Precision measures positive prediction reliability; recall measures coverage of actual positives.",
	"training workflow": "A training workflow turns raw data, code, configuration, and validation into a reproducible model artifact.",
	"artifacts": "Artifacts are versioned outputs such as models, encoders, schemas, reports, and evaluation results.",
	"schemas": "Schemas define names, types, constraints, and required fields at data and service boundaries.",
	"model cards": "Model cards record intended use, data, evaluation, limitations, risks, and release decisions.",
	"REST inference": "REST inference exposes model predictions through versioned HTTP endpoints with explicit request contracts.",
	"contract tests": "Contract tests prove that producers and consumers agree on request, response, and error behavior.",
	"logging": "Logging captures structured events needed to diagnose behavior without reproducing every request.",
	"drift": "Drift is a change in inputs, relationships, or outcomes that can invalidate historical performance.",
	"tokens": "Tokens are the discrete text units a language model consumes and produces.",
	"context windows": "A context window limits how much prompt, retrieved evidence, and generated text a model can consider.",
	"prompt contracts": "Prompt contracts specify role, task, evidence, constraints, and output format as a testable interface.",
	"evaluation": "Evaluation measures output quality against representative cases, explicit criteria, and failure thresholds.",
	"embeddings": "Embeddings map content into vectors whose geometric proximity can represent semantic similarity.",
	"retrieval": "Retrieval selects evidence from an indexed collection before generation or decision-making.",
	"grounding": "Grounding ties an answer to supplied evidence so claims can be checked against a source.",
	"guardrails": "Guardrails constrain inputs, tool use, outputs, and escalation paths around a model.",
	"joins": "Joins combine rows from related tables using matching keys and a declared inclusion rule.",
	"window functions": "Window functions compute values across related rows without collapsing the result grain.",
	"grain": "Grain states what one row represents and determines which joins and aggregations are valid.",
	"dimensional modelling": "Dimensional modelling organizes facts and dimensions around stable analytical questions.",
	"partitions": "Partitions divide distributed data so storage and computation can be pruned and parallelized.",
	"lazy evaluation": "Lazy evaluation records transformations and executes them only when an action requires a result.",
	"shuffles": "A shuffle redistributes records across workers and is often the dominant cost in distributed processing.",
	"distributed joins": "Distributed joins choose broadcast, shuffle, or partition-aware strategies to combine large datasets.",
	"Docker": "Docker packages an application and runtime dependencies into a reproducible container image.",
	"configuration": "Configuration separates environment-specific values from versioned application behavior.",
	"CI and CD": "Continuous integration and delivery automate validation and controlled release of versioned changes.",
	"cloud services": "Cloud services provide managed compute, storage, networking, identity, and observability primitives.",
	"experiment tracking": "Experiment tracking links parameters, code, data, metrics, and artifacts for each training run.",
	"model registry": "A model registry controls versioned model stages, metadata, approvals, and deployment references.",
	"promotion": "Promotion moves a validated artifact between environments without rebuilding it.",
	"observability": "Observability combines metrics, logs, and traces to explain system behavior in production.",
	"audience": "Audience defines the decisions, prior knowledge, constraints, and level of detail a communication must serve.",
	"narrative": "Narrative orders evidence so each step creates the need for the next and resolves a central question.",
	"visual hierarchy": "Visual hierarchy uses position, scale, contrast, and spacing to direct attention in the intended order.",
	"uncertainty": "Uncertainty describes what is not known, how large the plausible range is, and what could change the conclusion.",
	"integration": "Integration proves that independently built components work together across real interfaces.",
	"demo design": "Demo design selects a credible path that exposes value, evidence, and failure handling without hiding risk.",
	"tradeoffs": "Tradeoffs make the benefits, costs, risks, and constraints of a choice explicit.",
	"roadmaps": "Roadmaps sequence outcomes, dependencies, and learning milestones rather than listing disconnected tasks.",
}

CONCEPT_DEFINITIONS.update(
	{
		"Python data structures": "Lists preserve ordered examples, dictionaries attach names to values, sets enforce uniqueness, and tuples represent fixed records.",
		"type hints": "Type hints document accepted and returned values so editors, static checks, and reviewers can expose incompatible data before execution.",
		"NumPy arrays": "NumPy arrays store one numerical dtype in a shaped buffer and apply vectorized operations across complete dimensions.",
		"invalid records": "Invalid records violate a declared type, range, relationship, or required-field rule and must be rejected or quarantined explicitly.",
		"vectors and matrices": "A vector represents one ordered feature set; a matrix stacks vectors so one operation can transform many examples.",
		"loss functions": "A loss function converts prediction error into a scalar objective whose definition determines what training rewards.",
		"gradients": "A gradient gives the local rate and direction of loss change for every trainable parameter.",
		"shape mismatch": "A shape mismatch means connected dimensions do not agree, usually revealing an incorrect feature, batch, or output contract.",
		"linear regression": "Linear regression estimates a weighted sum of features that minimizes residual error under explicit statistical assumptions.",
		"preprocessing pipelines": "A preprocessing pipeline learns transformations from training data and reapplies the same fitted operations during validation and inference.",
		"coefficients": "A fitted coefficient is the expected output change for a one-unit feature change while other encoded features remain fixed.",
		"data leakage": "Data leakage occurs when training receives information unavailable at the real prediction time, producing unrealistically strong evaluation.",
		"tensors": "A tensor is a typed, multidimensional array that can live on CPU or accelerator memory and participate in differentiable operations.",
		"autograd": "Autograd records tensor operations and applies the chain rule backward to calculate parameter gradients.",
		"training loops": "A training loop repeats batch loading, forward prediction, loss calculation, gradient reset, backpropagation, and optimizer update.",
		"missing eval mode": "Without evaluation mode, dropout remains random and batch-normalization statistics keep changing during validation.",
		"data profiling": "Data profiling summarizes schema, missingness, ranges, categories, duplicates, and target balance before modelling decisions are made.",
		"distributions": "A distribution reveals center, spread, skew, modes, and extremes that a single average cannot show.",
		"feature importance": "Feature importance ranks predictive contribution under a particular model; it does not establish causal effect.",
		"silent data drift": "Silent data drift changes input frequencies or relationships without breaking the schema, so valid requests can still become unreliable.",
		"Pandera schemas": "A Pandera schema expresses dataframe columns, dtypes, nullability, ranges, and cross-column checks as executable Python contracts.",
		"feature pipelines": "A feature pipeline binds fitted imputers, encoders, and scalers into the same artifact used by training and serving.",
		"DVC": "DVC versions large data and model artifacts by storing lightweight hashes in Git and declaring reproducible pipeline stages.",
		"schema drift": "Schema drift is an incompatible change to column presence, type, range, or category rules at a data boundary.",
		"training pipelines": "A training pipeline makes every step from versioned data to evaluated model an explicit dependency with a reproducible command.",
		"experiment tracking": "Experiment tracking links parameters, code revision, data revision, metrics, and artifacts to one immutable run.",
		"model selection": "Model selection chooses a candidate using validation evidence and business constraints while leaving final test data untouched.",
		"untracked data version": "An untracked data version breaks reproducibility because identical code and parameters can train on different examples.",
		"REST contracts": "A REST contract defines the endpoint, method, typed request, typed response, status codes, and compatibility behavior.",
		"Pydantic models": "Pydantic models parse and validate untrusted request data into typed Python objects with structured error details.",
		"container images": "A container image is an immutable filesystem and runtime specification built in layers from a declared base.",
		"training-serving skew": "Training-serving skew occurs when online preprocessing or feature definitions differ from those used to fit the model.",
		"ECR images": "Amazon ECR stores versioned OCI images and immutable digests that deployment systems can pull through IAM.",
		"EC2 deployment": "An EC2 deployment runs the container on a managed virtual machine whose compute, networking, storage, and patching remain explicit.",
		"IAM roles": "An IAM role supplies temporary, scoped AWS credentials to a workload without embedding long-lived keys.",
		"unbounded cloud cost": "Unbounded cloud cost results when compute, storage, logs, traffic, or model calls lack budgets, quotas, and lifecycle limits.",
		"local inference": "Local inference executes model weights on the learner's hardware, trading managed scale for privacy, control, and hardware limits.",
		"model manifests": "A model manifest records architecture, parameterization, quantization, template, context limits, and immutable model identity.",
		"streaming": "Streaming returns incremental output as it is generated, reducing perceived latency while requiring framed events and cancellation handling.",
		"model memory pressure": "Model memory pressure appears when weights, context cache, and runtime buffers exceed available RAM or accelerator memory.",
		"instruction hierarchy": "Instruction hierarchy resolves conflicts by separating trusted system and developer rules from user requests and untrusted content.",
		"few-shot examples": "Few-shot examples demonstrate the exact input-output behavior expected from the model without changing its weights.",
		"output contracts": "An output contract fixes required fields, types, allowed values, and failure behavior so downstream code can validate a response.",
		"prompt injection": "Prompt injection occurs when untrusted content attempts to override instructions or trigger tools beyond the user's authorized task.",
		"provider APIs": "Provider APIs expose model inference through differing names, message formats, capabilities, limits, and usage metadata.",
		"structured output": "Structured output constrains a model response to a machine-validated schema instead of relying on prose parsing.",
		"tool calling": "Tool calling lets a model propose a named operation and arguments; application code remains responsible for validation and execution.",
		"unsafe tool arguments": "Unsafe tool arguments are model-produced values that exceed the user's authorization, schema, path, query, or resource limits.",
		"messages": "Messages preserve role and conversational order so instructions, user input, tool calls, and tool results remain distinguishable.",
		"retrieval chains": "A retrieval chain transforms a question into evidence, assembles context, calls the model, and returns a traceable answer.",
		"hidden framework retries": "Hidden framework retries repeat model calls behind an abstraction, changing latency and cost unless call counts are traced.",
		"MCP servers": "An MCP server advertises narrowly scoped resources, prompts, and tools through a standard capability protocol.",
		"tools and resources": "MCP tools perform actions, while resources expose addressable context that a client can read under declared permissions.",
		"transports": "An MCP transport carries protocol messages, commonly over local standard I/O or networked HTTP with different trust boundaries.",
		"excessive tool permissions": "Excessive tool permissions grant an integration access beyond the task, increasing the impact of mistakes and prompt injection.",
		"teacher models": "A teacher model generates provisional labels or demonstrations that a smaller task model can learn from.",
		"label schemas": "A label schema fixes class meanings, allowed values, confidence fields, and annotation rules before data generation begins.",
		"quality sampling": "Quality sampling selects a stratified human-review subset to estimate label errors across classes and difficult cases.",
		"teacher bias": "Teacher bias is systematic annotation behavior inherited from the teacher model, prompt, or examples.",
		"DSPy signatures": "A DSPy signature declares a program's typed inputs and outputs while leaving prompt construction to the compiler.",
		"teleprompters": "DSPy optimizers search demonstrations and instructions that improve a declared metric on development examples.",
		"held-out evaluation": "Held-out evaluation measures the final frozen program on examples never used for fitting, compiling, or threshold selection.",
		"test-set optimization": "Test-set optimization repeatedly changes a system after viewing test results, turning the test set into training feedback.",
		"evaluation datasets": "An evaluation dataset represents real tasks, edge cases, and expected behavior in a versioned, reviewable collection.",
		"task metrics": "Task metrics translate useful behavior into measurable checks such as correctness, groundedness, refusal, latency, or cost.",
		"LLM judges": "An LLM judge applies a scoring rubric to model output but must be calibrated against human decisions.",
		"judge leakage": "Judge leakage exposes references or expected answers in a way that lets the evaluator reward superficial matching.",
		"instruction data": "Instruction data pairs a task request with the desired response format and behavior used during supervised adaptation.",
		"LoRA adapters": "LoRA learns small low-rank updates beside frozen base weights, reducing memory and storage required for task adaptation.",
		"training evaluation": "Training evaluation compares the unchanged base and adapted model on held-out task, safety, latency, and general-capability cases.",
		"catastrophic forgetting": "Catastrophic forgetting is the loss of useful general behavior when adaptation over-specializes model parameters.",
		"chat messages": "Chat messages encode role, content, and order so a model can distinguish instructions from conversation and tool results.",
		"conversation memory": "Conversation memory selects or summarizes prior turns that remain relevant to the next response.",
		"streaming UI": "A streaming UI renders framed partial events, preserves state, handles cancellation, and reports terminal errors.",
		"unbounded context growth": "Unbounded context growth increases tokens and latency until relevant information is diluted or evicted.",
		"full-context generation": "Full-context generation places the complete small corpus in the prompt instead of selecting chunks with a retriever.",
		"prefix caching": "Prefix caching reuses model computation for an unchanged leading prompt, reducing repeated full-context cost.",
		"context budgets": "A context budget allocates the finite token window among instructions, evidence, history, tool results, and response.",
		"stale corpus": "A stale corpus differs from the current source of truth because refresh and invalidation were not enforced.",
		"PDF parsing": "PDF parsing reconstructs text, tables, images, and reading order from a format designed primarily for visual layout.",
		"layout structure": "Layout structure preserves headings, columns, tables, captions, and block order needed to interpret extracted content.",
		"provenance": "Provenance records the source file, page, section, parser, and stable identifier behind every extracted block.",
		"silent extraction loss": "Silent extraction loss omits or corrupts content without raising an error, leaving an apparently valid but incomplete corpus.",
		"chunk boundaries": "Chunk boundaries decide which neighboring words and structural units can be retrieved together as one evidence block.",
		"overlap": "Overlap repeats text across adjacent chunks to preserve boundary context at the cost of storage and duplicate retrieval.",
		"semantic chunking": "Semantic chunking places boundaries where embedding or model signals indicate a topic change.",
		"duplicated context": "Duplicated context wastes the prompt budget and can overweight one passage when overlapping chunks are retrieved together.",
		"embeddings": "Embeddings map content into fixed-length vectors whose geometry can approximate semantic similarity.",
		"cosine similarity": "Cosine similarity compares vector direction after normalization, reducing sensitivity to vector magnitude.",
		"pgvector indexes": "pgvector supports exact search and approximate HNSW or IVFFlat indexes with different recall, build, and latency tradeoffs.",
		"cross-tenant retrieval": "Cross-tenant retrieval returns content outside the caller's authorization because filtering was omitted or applied too late.",
		"BM25": "BM25 ranks documents by query-term frequency, document length, and term rarity, making it strong for exact identifiers.",
		"rank fusion": "Rank fusion combines independent ordered result lists without assuming their raw scores share a scale.",
		"reranking": "Reranking applies a more expensive query-document model to a small candidate set to improve final ordering.",
		"incompatible score scales": "Lexical, vector, and reranker scores have different meanings, so direct arithmetic can produce unstable rankings.",
		"RAG pipelines": "A RAG pipeline ingests sources, chunks and indexes them, retrieves evidence, assembles context, generates, and validates citations.",
		"context assembly": "Context assembly orders, deduplicates, labels, and truncates retrieved evidence inside a fixed prompt budget.",
		"citations": "Citations identify the exact source and location supporting a generated claim and must be checked against returned evidence.",
		"unsupported answers": "An unsupported answer makes claims absent from retrieved evidence and should be rejected or marked insufficient.",
		"graph state": "Graph state is the typed record passed between nodes and persisted at checkpoints during an execution.",
		"nodes and edges": "Nodes perform bounded work; edges define the explicit transitions that control execution order.",
		"conditional routing": "Conditional routing selects the next node from inspected state instead of allowing unconstrained model control.",
		"unbounded graph loops": "An unbounded graph loop can repeat model or tool calls indefinitely unless attempts and total steps are capped.",
		"multi-step workflows": "A multi-step workflow decomposes a task into inspectable stages with declared inputs, outputs, and transitions.",
		"specialized roles": "Specialized roles constrain each node to one responsibility, such as collection, analysis, or synthesis.",
		"shared state": "Shared state carries evidence and decisions between roles without relying on hidden conversational memory.",
		"fabricated evidence": "Fabricated evidence is a claim or citation not traceable to collected source records.",
		"tool selection": "Tool selection chooses an operation whose capability and risk match the current subtask.",
		"SQL generation": "SQL generation translates a question into a query against an inspected schema under read-only and resource constraints.",
		"result interpretation": "Result interpretation explains returned rows at their correct grain without inventing missing causes or context.",
		"unsafe database writes": "Unsafe database writes modify state through generated SQL when the task only authorized analysis.",
		"MCP clients": "An MCP client discovers server capabilities, requests resources or tools, and returns results to the application graph.",
		"filesystem resources": "Filesystem resources expose approved files through stable identifiers while enforcing root, type, and size limits.",
		"agent routing": "Agent routing chooses whether to retrieve, call a tool, ask for clarification, or finish based on typed state.",
		"path traversal": "Path traversal uses parent segments or links to escape an approved filesystem root.",
		"planning": "Planning decomposes a complex question into evidence requirements and ordered tool operations before synthesis.",
		"financial tools": "Financial tools retrieve timestamped prices, filings, and calculated indicators with explicit symbols and reporting periods.",
		"agentic retrieval": "Agentic retrieval lets a graph decide which source and query to use while preserving limits and an evidence ledger.",
		"unsupported financial claims": "Unsupported financial claims combine stale, mismatched, or uncited evidence into advice that the system cannot justify.",
	}
)

CONCEPT_DEFINITIONS.update(
	{
		"algorithms": "An algorithm is a finite, ordered set of unambiguous steps that transforms an input into an output.",
		"variables": "A variable is a name bound to a value so a program can reuse or replace that value.",
		"expressions": "An expression combines values, variables, and operators to calculate a new value.",
		"syntax errors": "A syntax error means Python cannot parse the written instructions according to its grammar.",
		"lists and dictionaries": "A list stores ordered values by position; a dictionary stores values under meaningful keys.",
		"conditions": "A condition evaluates to true or false and controls which branch of code executes.",
		"loops": "A loop repeats a block for each item or while a stated condition remains true.",
		"arrays and shapes": "An array stores same-type values along axes; its shape gives the length of each axis.",
		"DataFrames": "A DataFrame is a labelled two-dimensional table whose rows are observations and columns are variables.",
		"filtering and grouping": "Filtering selects rows by a condition; grouping partitions rows before applying an aggregation.",
		"descriptive statistics": "Descriptive statistics summarize the center, spread, frequency, and extremes of observed values.",
		"correlation and causation": "Correlation measures association; causation requires evidence that changing one factor changes another.",
		"supervised and unsupervised learning": "Supervised learning uses known targets; unsupervised learning searches for structure without target labels.",
		"regression and classification": "Regression predicts a continuous quantity; classification predicts a category or category probability.",
		"training and inference": "Training estimates model parameters from examples; inference applies fixed learned parameters to new inputs.",
		"generalization": "Generalization is useful performance on representative examples that did not influence model fitting.",
		"continuous targets": "A continuous target can take numerical values across an interval, such as price, temperature, or body-fat percentage.",
		"linear equation": "A linear prediction adds an intercept to feature values multiplied by learned coefficients.",
		"residuals and RMSE": "A residual is actual minus predicted; RMSE summarizes squared residuals in the target's original units.",
		"probabilities and thresholds": "A probability represents uncertainty; a threshold converts that probability into an action or class.",
		"confusion matrix": "A confusion matrix counts correct and incorrect predictions for each actual and predicted class.",
		"layers and activations": "A layer computes weighted sums; an activation introduces a nonlinear transformation.",
		"backpropagation": "Backpropagation applies the chain rule from loss to every trainable parameter.",
		"training and evaluation modes": "Training mode enables learning-time behavior; evaluation mode freezes stochastic or running-statistic behavior.",
		"imputation and encoding": "Imputation replaces declared missing values; encoding converts categories into numerical model inputs.",
		"ColumnTransformer and Pipeline": "ColumnTransformer applies column-specific operations; Pipeline binds preprocessing and estimation in order.",
		"experiment artifacts": "Experiment artifacts are versioned models, preprocessors, metrics, reports, and configurations produced by a run.",
		"HTTP and JSON": "HTTP defines request and response exchange; JSON represents structured values in the message body.",
		"FastAPI contracts": "A FastAPI contract declares an endpoint's method, typed request, response, and error behavior.",
		"Docker containers": "A Docker container runs an application inside the filesystem and dependencies fixed by its image.",
		"AWS operations": "AWS operations cover scoped identity, networking, compute, logs, health, budgets, and controlled rollback.",
		"tokens and context windows": "Tokens are model vocabulary units; the context window limits how many input and output tokens can be considered.",
		"next-token prediction": "An LLM assigns probabilities to possible next tokens from the tokens already in context.",
		"logits and softmax": "Logits are raw token scores; softmax converts them into positive probabilities that sum to one.",
		"base and instruction models": "A base model predicts text continuations; an instruction model is adapted to follow conversational tasks.",
		"message roles": "Message roles distinguish trusted instructions, user requests, assistant output, and tool results.",
		"instructions and examples": "Instructions state required behavior; examples demonstrate the exact input-output pattern.",
		"JSON schemas": "A JSON schema defines required fields, types, allowed values, and nesting for machine-validated output.",
		"streaming and retries": "Streaming returns partial events; retries repeat only transient failures under explicit count and time limits.",
		"LangChain components": "LangChain components connect model calls, prompts, retrieval, tools, parsers, and traces behind explicit interfaces.",
		"Model Context Protocol": "MCP standardizes how applications expose scoped tools and resources to model clients.",
		"document processing and chunking": "Document processing extracts structured content; chunking divides it into retrievable evidence units.",
		"vector search": "Vector search ranks stored embeddings by geometric similarity to an embedded query.",
		"grounded generation and citations": "Grounded generation uses supplied evidence; citations identify which evidence supports each claim.",
		"retrieval precision and recall": "Retrieval precision measures result relevance; retrieval recall measures coverage of all relevant evidence.",
		"hybrid search and reranking": "Hybrid search combines lexical and semantic candidates; reranking applies a stronger model to reorder them.",
		"groundedness": "Groundedness measures whether generated claims are supported by the context supplied to the model.",
		"evaluation datasets and judges": "Evaluation datasets represent real tasks; judges apply explicit rubrics that must be checked against humans.",
		"workflows and agents": "A workflow follows declared control flow; an agent chooses actions dynamically from observations and goals.",
		"state nodes and edges": "State stores the run record, nodes transform it, and edges define allowed transitions.",
		"tools and observations": "A tool performs a bounded operation; its returned observation becomes evidence for the next decision.",
		"checkpoints and stopping conditions": "Checkpoints persist resumable state; stopping conditions bound attempts, steps, time, and cost.",
		"requirements and architecture": "Requirements define testable needs and constraints; architecture assigns them to components and interfaces.",
		"evidence-first implementation": "Evidence-first implementation defines observable acceptance checks before building a successful demo path.",
		"evaluation and observability": "Evaluation measures expected behavior; observability records live metrics, logs, and traces.",
		"security cost and deployment": "Production release constrains permissions, secrets, resources, budgets, health, and rollback.",
	}
)


CODE_EXAMPLES = {
	"Python for Data Science I": """def summarize(values):
    clean = [value for value in values if value is not None]
    if not clean:
        raise ValueError("No valid observations")
    return {"count": len(clean), "mean": sum(clean) / len(clean)}

summary = summarize([14, 18, None, 21])""",
	"Python for Data Science II: NumPy": """import numpy as np

sales = np.array([[12, 18, 15], [9, 14, 20]])
monthly_total = sales.sum(axis=0)
growth = np.diff(monthly_total) / monthly_total[:-1]
high_growth = growth > 0.15""",
	"Git and Reproducible Project Structure": """project/
  pyproject.toml
  src/dsacademy/
  tests/
  notebooks/
  data/README.md

$ git switch -c feature/data-contract
$ pytest && git commit -m "add data contract\"""",
	"APIs and Interactive Data Apps": """@app.post("/predict")
def predict(request: PredictionRequest):
    features = request.model_dump()
    result = model.predict_one(features)
    return {"prediction": result, "model_version": MODEL_VERSION}""",
	"Data Cleaning with Pandas": """rules = {
    "customer_id": "string",
    "signup_date": "datetime64[ns]",
    "monthly_spend": "float64",
}

clean = raw.assign(signup_date=lambda x: pd.to_datetime(x.signup_date))
assert clean.customer_id.notna().all()""",
	"Exploratory Data Analysis": """summary = (
    df.groupby("segment")
      .agg(customers=("customer_id", "nunique"),
           churn_rate=("churned", "mean"),
           median_spend=("spend", "median"))
      .sort_values("churn_rate", ascending=False)
)""",
	"Feature Engineering by Data Type": """features = events.assign(
    tenure_days=lambda x: (cutoff - x.signup_date).dt.days,
    is_weekend=lambda x: x.event_time.dt.dayofweek >= 5,
    spend_per_order=lambda x: x.spend / x.orders.clip(lower=1),
)
assert (features.event_time <= cutoff).all()""",
	"Reliable scikit-learn Pipelines": """pipeline = Pipeline([
    ("prepare", ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])),
    ("model", LogisticRegression(max_iter=1000)),
])
pipeline.fit(X_train, y_train)""",
	"Linear Regression and Baselines": """baseline = DummyRegressor(strategy="median")
model = LinearRegression()

baseline.fit(X_train, y_train)
model.fit(X_train, y_train)
results = compare_mae(baseline, model, X_test, y_test)""",
	"Regularized and Nonlinear Regression": """models = {
    "ridge": Ridge(alpha=1.0),
    "lasso": Lasso(alpha=0.01),
    "boosting": HistGradientBoostingRegressor(),
}
scores = cross_validate(models, X_train, y_train, metric="mae")""",
	"Validation, Cross-Validation and Tuning": """cv = TimeSeriesSplit(n_splits=5)
search = GridSearchCV(
    estimator=pipeline,
    param_grid={"model__max_depth": [3, 6, None]},
    scoring="neg_mean_absolute_error",
    cv=cv,
)
search.fit(X_train, y_train)""",
	"Metrics, Error Analysis and Responsible Evaluation": """report = evaluate(
    predictions,
    metrics=["precision", "recall", "calibration"],
    slices=["region", "channel", "customer_tier"],
)
release = report.meets_thresholds(policy)""",
	"Logistic Regression, Probability and Thresholds": """probability = model.predict_proba(X_valid)[:, 1]
thresholds = np.linspace(0.1, 0.9, 17)
policy = choose_threshold(
    y_valid, probability, thresholds,
    false_negative_cost=8, false_positive_cost=1,
)""",
	"Trees, Ensembles and Imbalanced Data": """model = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_leaf_nodes=31,
    class_weight="balanced",
)
model.fit(X_train, y_train)
evaluate_by_class(model, X_test, y_test)""",
	"End-to-End Classification Workflow": """run = train(
    data_version="customers-2026-07",
    config="configs/churn.yaml",
)
assert run.metrics["recall"] >= 0.78
registry.register(run.model, schema=run.schema, card=run.card)""",
	"Serving, Testing and Monitoring": """response = client.post("/v1/predict", json=valid_payload)
assert response.status_code == 200
assert set(response.json()) == {"prediction", "probability", "model_version"}

monitor.observe(response.json(), latency_ms=response.elapsed_ms)""",
	"LLM Foundations and Prompt Design": """prompt = {
    "role": "You answer from supplied policy excerpts.",
    "task": user_question,
    "evidence": retrieved_passages,
    "constraints": ["Cite evidence", "State when evidence is insufficient"],
    "output": {"answer": "string", "citations": "list"},
}""",
	"Embeddings, RAG and Guardrails": """query_vector = embed(question)
matches = index.search(query_vector, top_k=5)
evidence = rerank(question, matches)[:3]
answer = generate(question=question, evidence=evidence)
assert citations_supported(answer, evidence)""",
	"SQL and Analytical Data Modelling": """select
  d.month,
  c.segment,
  sum(f.revenue) as revenue,
  count(distinct f.customer_id) as customers
from fact_orders f
join dim_date d using (date_key)
join dim_customer c using (customer_key)
group by 1, 2;""",
	"Spark and Distributed ETL": """orders = spark.read.parquet(INPUT)
clean = orders.filter("amount > 0").repartition("order_date")
daily = clean.groupBy("order_date").agg(
    F.sum("amount").alias("revenue"),
    F.countDistinct("customer_id").alias("customers"),
)
daily.write.mode("overwrite").partitionBy("order_date").parquet(OUTPUT)""",
	"Containers, Cloud Architecture and CI": """FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY src ./src
CMD ["uv", "run", "gunicorn", "app:api"]

# CI: test -> build once -> scan -> promote""",
	"Experiments, Versioning and Monitoring": """with tracker.start_run() as run:
    run.log_params(config)
    model, metrics = train(config, data_version)
    run.log_metrics(metrics)
    run.log_artifact(model)

registry.promote(run.model_id, stage="staging")""",
	"Decision-Centred Data Storytelling": """story = {
    "decision": "Which retention action should we fund?",
    "evidence": segment_results,
    "uncertainty": confidence_intervals,
    "recommendation": selected_action,
    "next_measurement": experiment_plan,
}""",
	"Capstone Integration and Demo": """make reproduce
make test
make build
make deploy-staging
make smoke-test

# Demo: question -> evidence -> decision -> limitations -> roadmap""",
}


RISK_HINTS = {
	"data": "Confirm the row meaning, units, missingness, and collection boundary before interpreting a result.",
	"validation": "Do not tune against the final test set or validate on data that could not exist at decision time.",
	"leakage": "Freeze the prediction timestamp and reject every feature created after that boundary.",
	"probability": "A high score is not automatically calibrated probability or a justified action.",
	"model": "Compare against a simple baseline and inspect errors before adding complexity.",
	"API": "Version the request and response schema and make invalid inputs fail clearly.",
	"prompt": "Treat prompts as interfaces: test representative cases and validate the output contract.",
	"retrieval": "Retrieved text is evidence only when it is relevant, current, and traceable to a source.",
	"SQL": "Declare table grain before joining; otherwise duplicated facts can silently inflate totals.",
	"Spark": "Inspect the physical plan and avoid unnecessary shuffles or tiny partitions.",
	"Docker": "Keep secrets outside the image and promote the same tested digest between environments.",
	"cloud": "Design around explicit cost, identity, recovery, and observability boundaries.",
	"narrative": "Start from the decision; remove detail that does not change the conclusion or next action.",
}

PANDAS_BIRDS_SOURCES = [
	"https://github.com/microsoft/Data-Science-For-Beginners/tree/main/2-Working-With-Data/07-python",
	"https://github.com/microsoft/Data-Science-For-Beginners/blob/main/data/birds.csv",
	"https://pandas.pydata.org/docs/getting_started/index.html",
	"https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html",
]


def build_pandas_birds_deck():
	"""Build the source-backed opening lesson around one real dataset."""
	slides = [
		{
			"kind": "cover",
			"title": "Exploratory Data Analysis with pandas",
			"subtitle": "Turn a 443-row birds CSV into checked, reproducible evidence.",
			"narration": "This lesson develops a complete exploratory workflow with pandas using a real birds dataset.",
		},
		{
			"kind": "statement",
			"title": "Start with a question, not a library",
			"body": "Which bird groups differ most in typical body mass, and can we trust the recorded measurement ranges?",
			"narration": "Our analysis has two concrete goals: compare typical body mass across bird groups and test whether the recorded ranges are internally consistent.",
		},
		{
			"kind": "outcomes",
			"title": "By the end of this lesson",
			"items": [
				"Load and inspect a CSV without guessing its structure.",
				"Filter, derive, group, and aggregate with pandas.",
				"Detect invalid ranges and explain a defensible result.",
			],
			"narration": "You will load and inspect a CSV, transform it with pandas, and detect data quality problems before interpreting results.",
		},
		{
			"kind": "dataset",
			"title": "The dataset: 443 North American birds",
			"subtitle": "13 columns describe taxonomy, conservation status, and measurement ranges.",
			"headers": ["Name", "Category", "Status", "Min mass", "Max mass"],
			"rows": [
				["Black-bellied whistling-duck", "Waterfowl", "LC", "652 g", "1,020 g"],
				["Fulvous whistling-duck", "Waterfowl", "LC", "712 g", "1,050 g"],
				["Snow goose", "Waterfowl", "LC", "2,050 g", "4,050 g"],
				["Ross's goose", "Waterfowl", "LC", "1,066 g", "1,567 g"],
			],
			"callout": "Unit of analysis: one bird species per row.",
			"narration": "The dataset has 443 species and 13 fields. Each row represents one species, so every aggregation must preserve that grain.",
		},
		{
			"kind": "code_output",
			"title": "Load first; inspect immediately",
			"code": """import pandas as pd

birds = pd.read_csv("birds.csv")

print(birds.shape)
print(birds.columns.tolist())""",
			"output": """(443, 13)

['Name', 'ScientificName', 'Category',
 'Order', 'Family', 'Genus',
 'ConservationStatus', 'MinLength',
 'MaxLength', 'MinBodyMass',
 'MaxBodyMass', 'MinWingspan',
 'MaxWingspan']""",
			"takeaway": "Shape establishes scale; column names establish the available evidence.",
			"narration": "Read the file, then inspect its shape and column names. This prevents assumptions about row count, naming, and available variables.",
		},
		{
			"kind": "concept",
			"title": "A DataFrame is a labelled table",
			"body": "Columns are variables, rows are observations, and the index identifies rows. Most pandas operations preserve this alignment.",
			"index": 1,
			"narration": "A DataFrame is a labelled table. In this dataset columns are variables, rows are species, and the index tracks row alignment.",
		},
		{
			"kind": "code_output",
			"title": "Select only the columns needed",
			"code": """view = birds.loc[
    :,
    ["Name", "Category",
     "ConservationStatus",
     "MinBodyMass", "MaxBodyMass"],
]

print(view.head(3))""",
			"output": """Name                         Category    Status  Min  Max
Black-bellied whistling-duck Waterfowl   LC      652 1020
Fulvous whistling-duck       Waterfowl   LC      712 1050
Snow goose                   Waterfowl   LC     2050 4050""",
			"takeaway": "A narrow analytical table is easier to reason about than all 13 columns.",
			"narration": "Use loc to select a deliberate analytical view. Keeping only required columns makes later transformations easier to verify.",
		},
		{
			"kind": "code_output",
			"title": "Filter rows with a boolean mask",
			"code": """at_risk = birds[
    birds["ConservationStatus"].isin(
        ["VU", "EN", "CR"]
    )
]

print(at_risk.shape[0])
print(at_risk["ConservationStatus"]
      .value_counts())""",
			"output": """13

VU    10
EN     2
CR     1""",
			"takeaway": "The condition is evaluated once per row; True rows remain.",
			"narration": "A boolean mask evaluates the condition for each species. Thirteen species are vulnerable, endangered, or critically endangered.",
		},
		{
			"kind": "pitfalls",
			"title": "Boolean filtering: two common mistakes",
			"items": [
				"Use & and | for element-wise logic, not Python's and and or.",
				"Wrap each comparison in parentheses before combining masks.",
				"Decide explicitly how missing boolean values should behave.",
			],
			"narration": "Use element-wise operators for Series conditions, parenthesize each comparison, and decide how missing values should be handled.",
		},
		{
			"kind": "code_output",
			"title": "Create a defensible derived feature",
			"code": """birds = birds.assign(
    BodyMassMidpoint=(
        birds["MinBodyMass"]
        + birds["MaxBodyMass"]
    ) / 2
)

print(birds["BodyMassMidpoint"]
      .describe().round(1))""",
			"output": """count      443.0
mean       497.5
std       1199.8
min          2.5
50%         73.0
max      11750.0""",
			"takeaway": "The median is far below the mean: body mass is strongly right-skewed.",
			"narration": "The midpoint summarizes each recorded mass range. The median is much lower than the mean, so a few very heavy species dominate the average.",
		},
		{
			"kind": "chart",
			"title": "Start with frequency: which groups dominate?",
			"chartType": "bar",
			"categories": [
				"Waterfowl",
				"Warblers",
				"Sandpipers",
				"Gulls",
				"Sparrows",
				"Flycatchers",
			],
			"series": [{"name": "Species", "values": [45, 41, 34, 28, 26, 19]}],
			"insight": "The six largest categories contain 193 of 443 species. Unequal group sizes matter when comparing distributions.",
			"narration": "Waterfowl and New World warblers are the largest categories. Unequal group sizes affect the stability of comparisons.",
		},
		{
			"kind": "concept",
			"title": "GroupBy is split, apply, combine",
			"body": "Split rows by category, apply a summary to each group, then combine one result per group.",
			"index": 2,
			"narration": "GroupBy follows split, apply, combine: split species into categories, compute a statistic, and combine the category-level results.",
		},
		{
			"kind": "code_output",
			"title": "Aggregate with named outputs",
			"code": """mass_by_group = (
    birds.groupby("Category")
    .agg(
        species=("Name", "count"),
        median_mass=("BodyMassMidpoint",
                     "median"),
    )
    .sort_values("species", ascending=False)
)

print(mass_by_group.head(6))""",
			"output": """Category                    species  median_mass
Ducks/Geese/Waterfowl            45        950.0
New World warblers               41         10.5
Sandpipers/Allies                34         79.0
Gulls/Terns/Skimmers             28        291.0
New World sparrows               26         21.6
Tyrant flycatchers               19         21.0""",
			"takeaway": "Named aggregation makes the output schema explicit.",
			"narration": "Named aggregation produces readable output columns. We retain group size alongside median mass so the summary has context.",
		},
		{
			"kind": "chart",
			"title": "Typical mass differs by almost 100×",
			"chartType": "bar",
			"categories": [
				"Waterfowl",
				"Gulls",
				"Sandpipers",
				"Sparrows",
				"Flycatchers",
				"Warblers",
			],
			"series": [{"name": "Median midpoint (g)", "values": [950, 291, 79, 21.6, 21, 10.5]}],
			"insight": "Among the six largest groups, waterfowl have the highest median mass midpoint. This describes the sample; it does not explain why.",
			"narration": "The median midpoint differs sharply across categories. Waterfowl are heaviest among the six largest groups, but the chart is descriptive rather than causal.",
		},
		{
			"kind": "statement",
			"title": "Before interpreting, test the data contract",
			"body": "For every recorded range, minimum must be less than or equal to maximum.",
			"narration": "Before trusting the result, test the range contract. Every minimum should be less than or equal to its corresponding maximum.",
		},
		{
			"kind": "code_output",
			"title": "Write the quality check as code",
			"code": """invalid = birds[
    (birds["MinLength"]
        > birds["MaxLength"])
    | (birds["MinBodyMass"]
        > birds["MaxBodyMass"])
    | (birds["MinWingspan"]
        > birds["MaxWingspan"])
]

print(invalid["Name"].tolist())""",
			"output": """['Brant',
 'American wigeon',
 'Long-billed murrelet']""",
			"takeaway": "A zero-row result is the passing condition. Here, three rows fail.",
			"narration": "The range check finds three species with at least one impossible minimum and maximum ordering.",
		},
		{
			"kind": "dataset",
			"title": "Inspect failures before choosing a repair",
			"subtitle": "The errors are localized, but the correct fix is not inferable from the CSV alone.",
			"headers": ["Species", "Field", "Recorded minimum", "Recorded maximum"],
			"rows": [
				["Brant", "Wingspan", "206 cm", "121 cm"],
				["American wigeon", "Wingspan", "76 cm", "71 cm"],
				["Long-billed murrelet", "Body mass", "310 g", "210 g"],
			],
			"callout": "Do not silently swap values unless provenance confirms they were reversed.",
			"narration": "Inspect each failure. We can identify invalid ordering, but source verification is required before deciding whether values were reversed or otherwise incorrect.",
		},
		{
			"kind": "verify",
			"title": "Choose a transparent repair policy",
			"items": [
				"Flag invalid ranges and preserve the original values.",
				"Exclude affected fields from calculations until verified.",
				"Document the rule, affected rows, and downstream impact.",
			],
			"narration": "A defensible temporary policy flags the rows, excludes affected fields, and preserves the original values for audit.",
		},
		{
			"kind": "chart",
			"title": "Conservation status is highly imbalanced",
			"chartType": "bar",
			"categories": ["LC", "NT", "VU", "EN", "CR", "EX"],
			"series": [{"name": "Species", "values": [402, 27, 10, 2, 1, 1]}],
			"insight": "90.7% are labelled Least Concern. Raw accuracy would be misleading in a later prediction task.",
			"narration": "Most species are labelled Least Concern. If this became a classification problem, class imbalance would make raw accuracy misleading.",
		},
		{
			"kind": "process",
			"title": "A reusable EDA loop",
			"items": ["Question", "Inspect", "Transform", "Validate"],
			"body": "Only interpret after the table grain, transformation, and quality checks are explicit.",
			"narration": "Use a repeatable loop: state the question, inspect the data, transform deliberately, validate assumptions, and only then interpret.",
		},
		{
			"kind": "code",
			"title": "Put the workflow in one reproducible script",
			"code": """import pandas as pd

birds = pd.read_csv("birds.csv")
birds["BodyMassMidpoint"] = (
    birds["MinBodyMass"]
    + birds["MaxBodyMass"]
) / 2

assert birds["Name"].is_unique

invalid_mass = (
    birds["MinBodyMass"]
    > birds["MaxBodyMass"]
)
analysis = birds.loc[~invalid_mass]

summary = (
    analysis.groupby("Category")
    .agg(species=("Name", "count"),
         median_mass=("BodyMassMidpoint",
                      "median"))
)""",
			"body": "Assertions and masks make quality decisions visible.",
			"narration": "A reproducible script makes the dataset, derived feature, uniqueness check, exclusion rule, and aggregation explicit.",
		},
		{
			"kind": "lab",
			"title": "Your turn: investigate wingspan",
			"body": "Which bird categories have the largest median wingspan midpoint after invalid ranges are excluded?",
			"items": ["Load", "Validate", "Aggregate", "Explain"],
			"narration": "Apply the same workflow to wingspan: load, validate, aggregate, visualize, and explain the result without causal overclaiming.",
		},
		{
			"kind": "code_output",
			"title": "Solution sketch",
			"code": """valid = birds[
    birds["MinWingspan"]
    <= birds["MaxWingspan"]
].copy()

valid["WingspanMidpoint"] = (
    valid["MinWingspan"]
    + valid["MaxWingspan"]
) / 2

answer = (
    valid.groupby("Category")
    ["WingspanMidpoint"]
    .median()
    .sort_values(ascending=False)
)""",
			"output": """Checks to include:
• Report the 2 excluded rows.
• Show group sizes with medians.
• Plot only a readable subset.
• State that results describe this dataset.""",
			"takeaway": "The solution is a reasoning sequence, not just a method chain.",
			"narration": "The solution filters invalid wingspan ranges, derives a midpoint, aggregates medians, and reports exclusions and limitations.",
		},
		{
			"kind": "quiz",
			"title": "Knowledge check",
			"items": [
				"Why is median more informative than mean for body mass here?",
				"What does a boolean mask represent?",
				"Why should the three invalid rows not be silently corrected?",
			],
			"narration": "Check your understanding of skew, boolean filtering, and transparent data repair.",
		},
		{
			"kind": "sources",
			"title": "What to retain",
			"items": [
				"State the analytical question and row grain.",
				"Pair every transformation with an inspectable output.",
				"Validate contracts before interpreting aggregates.",
				"Describe evidence without claiming unsupported causality.",
			],
			"source_labels": [
				"Microsoft Data Science for Beginners",
				"Working with Python and pandas lesson (MIT)",
				"North American birds dataset (MIT)",
				"Official pandas getting started and GroupBy guides",
			],
			"narration": "Retain the workflow: question, inspect, transform, validate, and interpret. The deck adapts MIT-licensed Microsoft curriculum with official pandas documentation.",
		},
	]
	for slide in slides:
		slide["sources"] = PANDAS_BIRDS_SOURCES
	assert len(slides) == 25
	return slides


def _risk_for(concept):
	for key, value in RISK_HINTS.items():
		if key.lower() in concept.lower():
			return value
	return f"Define how {concept} will be checked before treating its output as trustworthy."


def _concept_definition(concept):
	return CONCEPT_DEFINITIONS.get(
		concept,
		f"{concept.capitalize()} is a working concept that must be tied to an explicit input, transformation, and evidence check.",
	)


def build_slide_outline(week_number, session_number, week_data, session_data):
	"""Return the approved 12-slide concept-first beginner lesson."""
	title = session_data["title"]
	concepts = session_data["concepts"]
	outcomes = session_data["outcomes"]
	example = session_data["example"]
	sources = session_data["sources"]
	terms = [
		f"{name}: {meaning}"
		for name, meaning in session_data["mechanism_terms"].items()
	]
	slides = [
		{
			"kind": "cover",
			"title": title,
			"subtitle": week_data["focus"],
			"narration": f"{title}. {session_data['summary']}",
		},
		{
			"kind": "statement",
			"title": "Start from what you already know",
			"body": session_data["prerequisites"],
			"items": outcomes,
			"narration": (
				f"The required starting point is {session_data['prerequisites'].lower()}. "
				f"By the end, you will {outcomes[0].lower()}"
			),
		},
		{
			"kind": "concept",
			"title": "The vocabulary of this topic",
			"body": session_data["summary"],
			"items": [
				f"{concept}: {_concept_definition(concept)}"
				for concept in concepts
			],
			"narration": "Define the language before using it: " + ", ".join(concepts) + ".",
		},
		{
			"kind": "map",
			"title": "How the concept works",
			"items": concepts,
			"body": session_data["mechanism"],
			"narration": session_data["mechanism"],
		},
		{
			"kind": "concept",
			"title": "Read every part of the mechanism",
			"body": session_data["mechanism"],
			"items": terms,
			"narration": "Every symbol or component has a job. " + " ".join(terms),
		},
		{
			"kind": "example_setup",
			"title": "Worked example by hand",
			"body": session_data["worked_example"],
			"items": ["Known values", "Apply the mechanism", "Interpret the result"],
			"narration": (
				"Work through the values before running code. "
				+ session_data["worked_example"]
			),
		},
		{
			"kind": "code_output",
			"title": "Map the concept to Python",
			"code": example["code"],
			"output": example["output"],
			"takeaway": "Each line corresponds to a concept already explained.",
			"narration": (
				"Connect the hand-worked mechanism to Python. "
				f"The observed output is {example['output']}"
			),
		},
		{
			"kind": "checklist",
			"title": "Build the complete mental model",
			"items": session_data["deepening"],
			"narration": " ".join(session_data["deepening"]),
		},
		{
			"kind": "map",
			"title": "Notebook readiness map",
			"items": concepts,
			"body": session_data["notebook_bridge"],
			"narration": (
				session_data["notebook_bridge"]
				+ " Predict what each section does before executing it."
			),
		},
		{
			"kind": "pitfalls",
			"title": "Common beginner mistakes",
			"items": session_data["common_mistakes"],
			"narration": " ".join(session_data["common_mistakes"]),
		},
		{
			"kind": "lab",
			"title": "Guided notebook exercise",
			"body": session_data["lab"],
			"items": session_data["guided_steps"],
			"narration": f"Predict, run, inspect, and explain. {session_data['lab']}",
		},
		{
			"kind": "summary",
			"title": "Recap and knowledge check",
			"items": outcomes,
			"body": session_data["deliverable"],
			"source_labels": ["Official documentation", "Open-source reference curriculum"],
			"narration": (
				f"Retain the connection between {', '.join(concepts)}. "
				f"Verification evidence: {example['verify']}"
			),
		},
	]
	for slide in slides:
		slide["sources"] = sources
	assert 10 <= len(slides) <= 12
	return slides
