"""The approved 18-week, zero-prerequisite DS Academy curriculum."""

BOOTCAMP = "https://github.com/curiousily/AI-Bootcamp"
RAW = f"{BOOTCAMP}/blob/master"

COURSE = {
	"title": "AI Engineering Bootcamp",
	"short_introduction": (
		"An 18-week, beginner-first path from writing a first Python program "
		"to building and deploying an evidence-grounded AI application."
	),
	"description": """
<p>Learn practical AI engineering from zero coding knowledge. Each week teaches
one coherent topic through concepts, visual explanations, worked calculations,
short code examples, and a guided lab based on selected MIT-licensed notebooks
from the curiousily AI Bootcamp.</p>
<p>Every three-hour lesson includes an English presentation of 10–12 substantive
slides, a worked example, a guided notebook, a knowledge check, and a practical
deliverable. Concepts are taught before libraries and notebook implementations.</p>
""".strip(),
	"tags": (
		"Python, Data Analysis, Machine Learning, PyTorch, MLOps, LLMs, "
		"RAG, LangChain, LangGraph, AI Agents, FastAPI, Docker, AWS"
	),
	"source_repository": BOOTCAMP,
	"source_license": "MIT",
	"source_revision": "e99fb571d355c368462c60cfaafa33061d3fe6bb",
	"duration_weeks": 18,
	"weekly_minutes": 180,
	"prerequisites": "None",
}


def notebook(name):
	return f"{RAW}/{name}.ipynb"


def topic(
	title,
	summary,
	concepts,
	prerequisites,
	mechanism,
	terms,
	worked_example,
	code,
	output,
	lab,
	deliverable,
	source_material,
	docs,
	mistakes,
	verify,
):
	"""Create one concept-first weekly lesson."""
	return {
		"title": title,
		"summary": summary,
		"build": lab,
		"prerequisites": prerequisites,
		"concepts": concepts,
		"mechanism": mechanism,
		"mechanism_terms": terms,
		"worked_example": worked_example,
		"notebook_bridge": (
			f"Use the concepts from this lesson to read and complete {source_material}."
		),
		"common_mistakes": mistakes,
		"guided_steps": ["Predict", "Run", "Inspect", "Explain"],
		"outcomes": [
			f"Explain {concepts[0]} in plain language.",
			f"Use {concepts[1]} in a small worked example.",
			f"Complete the guided lab and verify {concepts[-1]}.",
		],
		"lab": lab,
		"deliverable": deliverable,
		"narration_en": (
			f"{summary} The lesson starts from {prerequisites.lower()}, explains "
			f"the mechanism step by step, and prepares learners for the guided notebook."
		),
		"example": {
			"code": code.strip(),
			"output": output.strip(),
			"failure": mistakes[0],
			"verify": verify,
		},
		"source_material": source_material,
		"modernization": (
			"Use current stable Python and library APIs while preserving the source "
			"notebook's educational objective."
		),
		"sources": [source_material, *docs],
	}


def week(number, lesson):
	"""Wrap one topic in one LMS chapter with a weekly assessment."""
	concepts = lesson["concepts"]
	quiz = [
		(
			f"W{number:02d}Q1: Which statement best describes {concepts[0]}?",
			[
				lesson["summary"],
				f"It is another name for {concepts[-1]}.",
				"It is a package that removes the need to understand inputs.",
				"It is only relevant after deployment.",
			],
			0,
		),
		(
			f"W{number:02d}Q2: Why does the worked example use {concepts[1]}?",
			[
				f"To make {lesson['mechanism'].lower()} observable step by step.",
				"To hide intermediate values.",
				"To replace the learning objective with syntax.",
				"To avoid checking the result.",
			],
			0,
		),
		(
			f"W{number:02d}Q3: What must be checked before the lab is complete?",
			[
				lesson["example"]["verify"],
				"Only that the final cell executed.",
				"Only that no exception was printed.",
				"That the code is longer than the example.",
			],
			0,
		),
	]
	return {
		"title": f"Week {number:02d}: {lesson['title']}",
		"focus": lesson["summary"],
		"sessions": [lesson],
		"quiz": quiz,
		"assignment": (
			f"Week {number:02d} practical",
			lesson["deliverable"],
			"Concept explanation 30%, correct implementation 30%, evidence 20%, "
			"reflection 10%, presentation 10%.",
		),
	}


PYTHON_DOCS = "https://docs.python.org/3/"
NUMPY_DOCS = "https://numpy.org/doc/stable/"
PANDAS_DOCS = "https://pandas.pydata.org/docs/"
SKLEARN_DOCS = "https://scikit-learn.org/stable/"
PYTORCH_DOCS = "https://docs.pytorch.org/docs/stable/"
FASTAPI_DOCS = "https://fastapi.tiangolo.com/"
OLLAMA_DOCS = "https://docs.ollama.com/"
LANGCHAIN_DOCS = "https://docs.langchain.com/oss/python/langchain/overview"
LANGGRAPH_DOCS = "https://docs.langchain.com/oss/python/langgraph/overview"
MCP_DOCS = "https://modelcontextprotocol.io/docs/getting-started/intro"


LESSONS = [
	topic(
		"Computational Thinking and Python Basics",
		"Learn how a computer follows explicit instructions and write a first Python program.",
		["algorithms", "variables", "expressions", "syntax errors"],
		"No prior coding knowledge",
		"An input is stored in variables, transformed by expressions, and displayed as output.",
		{"variable": "A named reference to a value.", "expression": "Values and operators that produce a result."},
		"Store a rectangle length of 5 and width of 3; multiply them and print an area of 15.",
		"""
length = 5
width = 3
area = length * width
print("Area:", area)
""",
		"Area: 15",
		"Write a program that converts study minutes into hours and remaining minutes.",
		"A runnable Python file with named inputs, a calculation, output, and comments explaining each line.",
		notebook("01.python-essentials-for-ai"),
		[PYTHON_DOCS],
		["Reading `=` as mathematical equality instead of assignment.", "Treating an error message as a failure rather than diagnostic evidence."],
		"Change the inputs, predict the output first, and confirm Python produces the predicted value.",
	),
	topic(
		"Python Data Structures and Program Logic",
		"Represent collections of values and control which instructions execute.",
		["lists and dictionaries", "conditions", "loops", "functions"],
		"Variables, values, expressions, and printed output",
		"Collections hold related values; control flow selects or repeats work; functions package reusable transformations.",
		{"list": "An ordered mutable collection.", "dictionary": "Named keys mapped to values.", "function": "Reusable code with inputs and an output."},
		"Filter three student scores, keep values at least 50, and compute the pass count.",
		"""
scores = [42, 68, 91]
passed = [score for score in scores if score >= 50]
print(len(passed), passed)
""",
		"2 [68, 91]",
		"Build a function that summarizes names and scores stored in dictionaries.",
		"A Python program using a list, dictionaries, a condition, a loop, and a function with a return value.",
		notebook("01.python-essentials-for-ai"),
		[PYTHON_DOCS],
		["Confusing a list position with a dictionary key.", "Printing inside every function instead of returning a reusable value."],
		"Test an empty collection, one failing score, and several passing scores.",
	),
	topic(
		"Data Analysis with NumPy and Pandas",
		"Move from individual Python values to arrays and tables that describe a dataset.",
		["arrays and shapes", "DataFrames", "filtering and grouping", "missing values"],
		"Python collections, conditions, loops, and functions",
		"NumPy applies one operation across shaped numerical arrays; Pandas labels rows and columns for tabular analysis.",
		{"shape": "The length of every array axis.", "row": "One observation.", "column": "One measured variable."},
		"Calculate the mean of three scores, then group a four-row table by course.",
		"""
import pandas as pd
df = pd.DataFrame({"course": ["AI", "AI", "Web"], "score": [70, 90, 60]})
print(df.groupby("course")["score"].mean())
""",
		"course\nAI     80.0\nWeb    60.0",
		"Load a small CSV, inspect its shape, filter valid rows, and calculate grouped summaries.",
		"A notebook that explains row grain, column meanings, filters, missing values, and two grouped results.",
		notebook("01.python-essentials-for-ai"),
		[NUMPY_DOCS, PANDAS_DOCS],
		["Applying an operation along the wrong array or DataFrame axis and misreading the result.", "Dropping missing rows without explaining what information is lost."],
		"Report the input and output shapes and independently check one grouped result by hand.",
	),
	topic(
		"Exploratory Data Analysis",
		"Describe a dataset, expose quality problems, and form questions before modelling.",
		["data types", "descriptive statistics", "distributions", "correlation and causation"],
		"DataFrames, filtering, grouping, and missing values",
		"EDA moves from schema and row grain to quality, center, spread, shape, relationships, and documented findings.",
		{"mean": "Sum divided by count.", "median": "Middle ordered value.", "distribution": "How frequently values occur."},
		"For incomes [20, 22, 24, 26, 200], compare mean 58.4 with median 24 and explain the outlier.",
		"""
values = pd.Series([20, 22, 24, 26, 200])
print(values.mean(), values.median())
""",
		"58.4 24.0",
		"Profile the Bank Marketing data and support three findings with statistics and plots.",
		"An EDA report covering schema, missing/sentinel values, distributions, class balance, relationships, and limitations.",
		notebook("02.exploratory-data-analysis"),
		[PANDAS_DOCS, "https://seaborn.pydata.org/"],
		["Treating `unknown` as a valid category without investigation.", "Claiming that correlation proves one variable causes another."],
		"Recalculate reported statistics and ensure every chart has a stated question and interpretation.",
	),
	topic(
		"Mathematics and Statistics for Machine Learning",
		"Build the numerical language used to represent data, measure error, and improve a model.",
		["vectors and matrices", "probability", "loss functions", "gradients"],
		"Basic arithmetic, Python expressions, arrays, and averages",
		"Matrix multiplication produces predictions; loss measures error; a gradient gives the direction of fastest local loss increase.",
		{"vector": "An ordered list of numbers.", "matrix": "A rectangular grid of numbers.", "gradient": "One derivative for each parameter."},
		"For x=[2,3], w=[0.4,-0.1], and b=0.2, calculate x·w+b=0.7, then compare with target 1.",
		"""
import numpy as np
x = np.array([2.0, 3.0])
w = np.array([0.4, -0.1])
prediction = x @ w + 0.2
print(prediction)
""",
		"0.7",
		"Calculate vector shapes, a dot product, squared error, and one parameter update with visible intermediate values.",
		"A mathematical notebook with hand calculations beside matching NumPy results.",
		f"{RAW}/README.md",
		[NUMPY_DOCS, "https://mml-book.github.io/"],
		["Multiplying arrays without checking compatible dimensions.", "Changing a parameter without connecting the update to loss."],
		"Check every array shape and compare an analytical gradient with a finite-difference estimate.",
	),
	topic(
		"Machine Learning Fundamentals",
		"Choose the correct learning problem before choosing an algorithm.",
		["supervised and unsupervised learning", "regression and classification", "training and inference", "generalization"],
		"Features, targets, tables, distributions, and basic mathematical functions",
		"A model learns a mapping or structure from training data and is judged on unseen examples that represent future use.",
		{"feature": "An input available at prediction time.", "target": "The value a supervised model learns to predict.", "label": "A categorical target."},
		"Classify house price as regression, spam detection as classification, and customer grouping as clustering.",
		"""
problems = {"price": "regression", "spam": "classification", "segments": "clustering"}
for name, kind in problems.items():
    print(name, kind)
""",
		"price regression\nspam classification\nsegments clustering",
		"Frame five business questions by identifying observation, features, target, learning type, and evaluation evidence.",
		"A problem-framing worksheet with justified learning types and train/validation/test boundaries.",
		notebook("03.model-development"),
		[SKLEARN_DOCS],
		["Calling every prediction problem classification.", "Evaluating on rows that influenced training or preprocessing."],
		"For each problem, verify the target type and explain what one unseen test row represents.",
	),
	topic(
		"Linear Regression",
		"Learn how regression predicts a continuous value with a fitted weighted sum.",
		["continuous targets", "linear equation", "residuals and RMSE", "regularization"],
		"Regression versus classification, vectors, averages, loss, training, and testing",
		"ŷ = β₀ + β₁x₁ + … + βₙxₙ; training chooses coefficients that minimize squared residuals.",
		{"ŷ": "Predicted continuous value.", "β₀": "Intercept.", "βⱼ": "Coefficient for feature j.", "xⱼ": "Feature value j."},
		"For hours=3, β₀=40 and β₁=10, predict 70; with actual 76, residual=6 and squared error=36.",
		"""
intercept, coefficient, hours = 40, 10, 3
prediction = intercept + coefficient * hours
residual = 76 - prediction
print(prediction, residual, residual**2)
""",
		"70 6 36",
		"Fit a baseline and linear regression, interpret coefficients, calculate RMSE, and inspect residuals.",
		"A fitted regression pipeline with equation explanation, baseline comparison, diagnostics, and saved artifact.",
		notebook("03.model-development"),
		[SKLEARN_DOCS, notebook("04.model-evaluation-techniques")],
		["Calling RMSE an accuracy percentage even though it is an error measured in target units.", "Interpreting a coefficient causally or without considering feature scaling."],
		"Beat a mean baseline on held-out data and check residuals for systematic structure.",
	),
	topic(
		"Classification and Model Evaluation",
		"Predict categories and measure the different consequences of classification errors.",
		["logistic regression", "probabilities and thresholds", "confusion matrix", "precision and recall"],
		"Classification versus regression, linear scores, probability, and test data",
		"P(y=1|x)=1/(1+e^-(β₀+βᵀx)); a threshold turns probability into a class decision.",
		{"probability": "A number from 0 to 1.", "threshold": "The action boundary.", "precision": "Correct positives among predicted positives.", "recall": "Found positives among actual positives."},
		"From TP=8, FP=2, FN=4, calculate precision=0.80, recall≈0.67, and F1≈0.73.",
		"""
tp, fp, fn = 8, 2, 4
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)
print(round(precision, 2), round(recall, 2), round(f1, 2))
""",
		"0.8 0.67 0.73",
		"Evaluate a binary classifier at two thresholds and explain the operational tradeoff.",
		"An evaluation notebook with a confusion matrix, metric calculations, threshold comparison, and recommendation.",
		notebook("04.model-evaluation-techniques"),
		[SKLEARN_DOCS],
		["Using accuracy for a rare but important class.", "Changing the threshold after viewing the final test result."],
		"Recalculate every metric from the confusion matrix and justify the selected threshold using error costs.",
	),
	topic(
		"Neural Networks and PyTorch",
		"Understand how layers of trainable parameters learn through forward and backward passes.",
		["tensors", "layers and activations", "backpropagation", "training and evaluation modes"],
		"Vectors, matrices, classification, loss functions, gradients, and learning rates",
		"z=Wx+b computes a layer; an activation transforms z; backpropagation applies the chain rule to calculate gradients.",
		{"tensor": "A typed multidimensional array.", "weight": "A trainable multiplier.", "activation": "A nonlinear transformation.", "epoch": "One pass over training data."},
		"Calculate z=2×0.5−0.2=0.8, apply ReLU to keep 0.8, then compare the output with its target.",
		"""
import torch
x = torch.tensor([2.0])
w = torch.tensor([0.5], requires_grad=True)
loss = (torch.relu(x * w - 0.2) - 1.0) ** 2
loss.backward()
print(round(loss.item(), 2), round(w.grad.item(), 2))
""",
		"0.04 -0.8",
		"Train a small classifier with DataLoader batches and evaluate it under inference mode.",
		"A PyTorch notebook showing shapes, forward pass, loss, gradients, optimizer updates, validation, and saved state.",
		notebook("02.real-world-pytorch"),
		[PYTORCH_DOCS],
		["Forgetting to clear accumulated gradients.", "Evaluating with dropout or batch normalization still in training mode."],
		"Confirm shapes at each boundary, decreasing training loss, finite gradients, and deterministic evaluation behavior.",
	),
	topic(
		"Reliable Machine-Learning Pipelines",
		"Bind validation, preprocessing, model selection, and serialization into a reproducible workflow.",
		["imputation and encoding", "ColumnTransformer and Pipeline", "cross-validation", "experiment artifacts"],
		"Data quality, training/test boundaries, regression, classification, and evaluation metrics",
		"Fit learns preprocessing and model parameters from each training fold; transform and predict reuse those fitted values.",
		{"imputation": "A declared replacement for missing values.", "pipeline": "An ordered fitted workflow.", "fold": "One cross-validation partition."},
		"Show why scaling all rows before the split leaks the test mean, then place scaling inside a Pipeline.",
		"""
model = make_pipeline(StandardScaler(), Ridge())
scores = cross_val_score(model, X, y, cv=5, scoring="neg_root_mean_squared_error")
print(f"folds={len(scores)}")
""",
		"folds=5",
		"Build a mixed-column Pipeline, compare candidates with cross-validation, refit the selected model, and serialize it.",
		"A reproducible training pipeline with schema checks, tracked parameters, validation metrics, and a loadable model.",
		notebook("03.model-development"),
		[SKLEARN_DOCS, "https://mlflow.org/docs/latest/"],
		["Fitting preprocessing before cross-validation.", "Selecting a model on the final test set."],
		"Re-run from raw data and confirm the same split, features, model configuration, and evaluation result.",
	),
	topic(
		"Serving and Deploying Models",
		"Turn a fitted model into a validated network service and run it safely in the cloud.",
		["HTTP and JSON", "FastAPI contracts", "Docker containers", "AWS operations"],
		"Python functions, dictionaries, validation, fitted pipelines, and inference",
		"Client → HTTP request → validated schema → model inference → JSON response; a container fixes the runtime environment.",
		{"endpoint": "A network address and HTTP method.", "schema": "Required fields and types.", "container": "A packaged application runtime."},
		"Send age=30 and income=50000 to `/predict`; validate types; return prediction and model version.",
		"""
@app.post("/predict")
def predict(request: PredictionRequest):
    value = model.predict([request.model_dump().values()])[0]
    return {"prediction": float(value), "model_version": "1"}
""",
		'{"prediction": 0.72, "model_version": "1"}',
		"Expose a model through FastAPI, containerize it, add health checks, and document a minimal free-tier EC2 deployment.",
		"A tested API, Docker image, deployment runbook, health endpoint, logs, budget alert, and rollback steps.",
		f"{RAW}/README.md",
		[FASTAPI_DOCS, "https://docs.docker.com/", "https://docs.aws.amazon.com/"],
		["Accepting malformed input and passing it to the model.", "Opening cloud ports broadly or omitting cost limits."],
		"Test valid, invalid, missing, and extreme inputs plus container health and a cold restart.",
	),
	topic(
		"Large Language Model Fundamentals",
		"Understand what an LLM predicts, how text becomes tokens, and why generation is uncertain.",
		["tokens and context windows", "next-token prediction", "logits and softmax", "base and instruction models"],
		"Python, vectors, probability, neural-network layers, and inference",
		"P(tokenᵢ|previous tokens)=softmax(logits); generation repeatedly samples or selects a next token.",
		{"token": "A vocabulary unit represented by an integer.", "logit": "An unnormalized model score.", "temperature": "A control on sampling sharpness."},
		"For logits [2,1,0], subtract 2, exponentiate, and normalize to approximately [0.665,0.245,0.090].",
		"""
import numpy as np
logits = np.array([2.0, 1.0, 0.0])
p = np.exp(logits - logits.max())
print(np.round(p / p.sum(), 3))
""",
		"[0.665 0.245 0.09 ]",
		"Tokenize a prompt, inspect next-token probabilities, and compare deterministic and sampled local generation.",
		"A local Ollama notebook documenting tokens, context, generation settings, outputs, and observed limitations.",
		notebook("05.llms-101"),
		[notebook("28.ollama-quickstart"), OLLAMA_DOCS],
		["Treating generated text as retrieved knowledge.", "Changing temperature without understanding that it changes sampling, not factual knowledge."],
		"Repeat deterministic generation, record token counts, and explain every generation parameter used.",
	),
	topic(
		"Prompt Engineering and Structured Outputs",
		"Design model inputs and output contracts that application code can validate.",
		["message roles", "instructions and examples", "JSON schemas", "tool calling"],
		"LLM generation, Python dictionaries, JSON, functions, and validation",
		"Trusted instructions define task and constraints; a schema defines allowed output; application code validates before acting.",
		{"system message": "Trusted application-level instructions.", "schema": "Required output fields and types.", "tool call": "A proposed operation and arguments."},
		"Extract `{name, score}` from one sentence, reject a missing score, then map a validated call to a Python function.",
		"""
class Result(BaseModel):
    name: str
    score: float = Field(ge=0, le=1)

result = Result.model_validate({"name": "baseline", "score": 0.82})
print(result.model_dump())
""",
		"{'name': 'baseline', 'score': 0.82}",
		"Create a prompt contract, validate structured output, and safely execute one allow-listed tool.",
		"A prompt test suite with success, malformed output, injection, unauthorized tool, and recovery cases.",
		notebook("13.llm-output-format"),
		[notebook("16.llm-function-calling"), "https://docs.pydantic.dev/latest/"],
		["Parsing important data from unconstrained prose.", "Executing model-produced tool arguments without authorization and validation."],
		"Run a fixed test set and confirm valid outputs parse while malformed and unauthorized requests fail safely.",
	),
	topic(
		"Engineering LLM Applications",
		"Build a reliable application boundary around model providers, frameworks, tools, and traces.",
		["provider APIs", "streaming and retries", "LangChain components", "Model Context Protocol"],
		"HTTP, JSON, schemas, LLM messages, structured output, and tool calling",
		"Application → provider adapter → model; tools remain application-controlled; traces record prompts, calls, latency, and usage.",
		{"provider": "A hosted or local inference service.", "stream": "Incremental response events.", "MCP": "A standard protocol for model-facing capabilities."},
		"Call two providers through one interface, require the same schema, and fall back only on retryable errors.",
		"""
response = completion(
    model="ollama/llama3.2",
    messages=[{"role": "user", "content": "Return one JSON status"}],
)
print(response.choices[0].message.content)
""",
		'{"status":"ready"}',
		"Build one traced application that streams output, validates a response, and invokes a scoped external capability.",
		"An LLM service with provider configuration, structured output, tool boundaries, traces, retry limits, and usage reporting.",
		notebook("26.multiple-llm-providers-with-litellm"),
		[notebook("27.langchain-foundations"), LANGCHAIN_DOCS, MCP_DOCS],
		["Retrying every error and multiplying cost.", "Granting an MCP server broader filesystem or network access than the task requires."],
		"Simulate timeout, rate limit, malformed output, and denied tool access while confirming bounded behavior.",
	),
	topic(
		"Retrieval-Augmented Generation",
		"Ground an LLM response in selected evidence retrieved from an external document collection.",
		["document processing and chunking", "embeddings", "vector search", "grounded generation and citations"],
		"LLMs, vectors, dot products, application pipelines, schemas, and evaluation",
		"cos(a,b)=(a·b)/(||a||||b||); retrieve similar chunks, assemble context, then generate only from that context.",
		{"chunk": "A retrievable passage plus metadata.", "embedding": "A semantic vector.", "citation": "A reference connecting a claim to evidence."},
		"For vectors [1,0] and [0.8,0.6], cosine similarity is 0.8; rank it above [0,1], whose score is 0.",
		"""
import numpy as np
a, b = np.array([1, 0]), np.array([0.8, 0.6])
score = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
print(score)
""",
		"0.8",
		"Parse a document, create chunks and embeddings, retrieve evidence, and produce a cited answer or refusal.",
		"A from-scratch RAG notebook with inspectable chunks, similarity scores, citations, and unanswerable tests.",
		notebook("17.rag-from-scratch"),
		[notebook("06.build-rag"), "https://github.com/pgvector/pgvector"],
		["Choosing chunk sizes without inspecting document structure.", "Accepting a fluent answer that has no supporting retrieved evidence."],
		"Trace every answer to retrieved chunks and verify each citation supports the associated claim.",
	),
	topic(
		"RAG Quality and LLM Evaluation",
		"Measure retrieval and generation separately so a failed answer can be diagnosed.",
		["retrieval precision and recall", "hybrid search and reranking", "groundedness", "evaluation datasets and judges"],
		"RAG ingestion, embeddings, retrieval, citations, and classification metrics",
		"Recall@k measures relevant evidence found; precision@k measures retrieved evidence that is relevant; generation metrics judge use of evidence.",
		{"top-k": "The number of retrieved candidates.", "reranker": "A second model that reorders candidates.", "groundedness": "Whether claims are supported by supplied context."},
		"At k=4, retrieving three relevant chunks when five exist gives precision 3/4 and recall 3/5.",
		"""
relevant_retrieved, retrieved, relevant_total = 3, 4, 5
print(relevant_retrieved / retrieved, relevant_retrieved / relevant_total)
""",
		"0.75 0.6",
		"Compare vector, keyword, hybrid, and reranked retrieval on a labelled question set and evaluate cited answers.",
		"An evaluation report separating ingestion, retrieval, context, generation, latency, and cost failures.",
		notebook("07.advanced-rag-with-llama-3-in-langchain"),
		[notebook("12.llm-evaluation"), LANGCHAIN_DOCS],
		["Changing retrieval and generation simultaneously, hiding which stage improved.", "Trusting an LLM judge without calibrating it against human decisions."],
		"Use fixed questions and relevance labels, report per-stage metrics, and manually audit judge disagreements.",
	),
	topic(
		"AI Agents and LangGraph Workflows",
		"Coordinate stateful steps and bounded tool use with explicit graph control.",
		["workflows and agents", "state nodes and edges", "tools and observations", "checkpoints and stopping conditions"],
		"LLM applications, structured output, tools, retries, state, and evaluation",
		"State enters a node, the node returns an update, edges choose the next node, and explicit limits bound execution.",
		{"state": "The typed data carried through a run.", "node": "One transformation of state.", "edge": "A permitted transition.", "checkpoint": "Saved resumable state."},
		"Route a ticket: billing goes to lookup, technical goes to diagnostics, and unknown goes to human review.",
		"""
def route(state):
    return {"billing": "lookup", "technical": "diagnose"}.get(
        state["category"], "human_review"
    )
""",
		"billing -> lookup",
		"Build a typed LangGraph workflow with conditional routing, one tool, a checkpoint, and a step limit.",
		"A tested graph with state schema, rendered routes, tool permissions, execution traces, and failure recovery.",
		notebook("29.langgraph-quickstart"),
		[notebook("18.langgraph-basics"), LANGGRAPH_DOCS],
		["Using an open-ended agent when deterministic routing is sufficient.", "Allowing a graph to revisit a node without a step or attempt limit."],
		"Test every route, denied tool access, timeout, checkpoint resume, and maximum-step termination.",
	),
	topic(
		"Production AI Capstone",
		"Combine requirements, data, models, retrieval, tools, evaluation, deployment, and documentation into one defensible system.",
		["requirements and architecture", "evidence-first implementation", "evaluation and observability", "security cost and deployment"],
		"All prior weeks",
		"User need → explicit contract → bounded components → evidence and evaluation → monitored deployment.",
		{"requirement": "A testable user need and constraint.", "architecture": "Components and data flow.", "evidence": "Observable proof of behavior."},
		"Turn “answer questions about reports” into ingestion, retrieval, citation, refusal, latency, and access-control requirements.",
		"""
acceptance = {
    "citation_support": 0.95,
    "retrieval_recall_at_5": 0.85,
    "p95_latency_seconds": 5,
    "monthly_budget_usd": 10,
}
print(acceptance)
""",
		"{'citation_support': 0.95, 'retrieval_recall_at_5': 0.85, 'p95_latency_seconds': 5, 'monthly_budget_usd': 10}",
		"Build and demonstrate a small deployed AI system with documented requirements, tests, traces, and limitations.",
		"A deployed capstone, source repository, architecture diagram, evaluation report, demo, runbook, and limitations statement.",
		notebook("19.langgraph-crypto-agents"),
		[notebook("14.sql-agents-with-llama3-crewai"), LANGGRAPH_DOCS],
		["Starting implementation before defining acceptance criteria.", "Demonstrating one successful path while hiding failure, security, or cost behavior."],
		"Run the complete acceptance suite from clean setup and show evidence for quality, safety, latency, and cost limits.",
	),
]

DEEPENING = {
	"Computational Thinking and Python Basics": [
		"An algorithm must terminate and produce the same result for the same stated inputs.",
		"`=` assigns a value; `==` asks whether two values are equal.",
		"Python evaluates `*` before `+`; parentheses make intended order explicit.",
		"Read an error from its final line, then inspect the reported file and line number.",
	],
	"Python Data Structures and Program Logic": [
		"Choose a list for ordered items, a set for uniqueness, and a dictionary for named fields.",
		"`if` selects; `for` repeats over items; `while` repeats while a condition stays true.",
		"A function contract states accepted inputs, returned output, and possible failures.",
		"Decompose a program into small functions that each perform one understandable transformation.",
	],
	"Data Analysis with NumPy and Pandas": [
		"One row must have a declared grain, such as one student, transaction, or day.",
		"Axis 0 moves down rows; axis 1 moves across columns in a two-dimensional table.",
		"A boolean mask contains one True/False decision per row and supports transparent filtering.",
		"Missing values require a reasoned policy: retain, impute, exclude, or collect again.",
	],
	"Exploratory Data Analysis": [
		"Use median and interquartile range when extreme values distort mean and standard deviation.",
		"A histogram shows distribution shape; a box plot emphasizes quartiles and potential outliers.",
		"Compare target rates across meaningful groups before proposing a predictive feature.",
		"EDA produces testable data-quality and modelling hypotheses, not final causal conclusions.",
	],
	"Mathematics and Statistics for Machine Learning": [
		"`(n,k) @ (k,m)` is valid because the shared dimension represents the same features.",
		"Variance measures average squared distance from the mean; standard deviation restores original units.",
		"A derivative is local slope; a gradient collects one local slope per parameter.",
		"Gradient descent moves opposite the gradient by a distance controlled by the learning rate.",
	],
	"Machine Learning Fundamentals": [
		"Regression targets are continuous; classification targets are categories; clustering has no supplied target.",
		"Training learns parameters, validation selects choices, and testing estimates final generalization.",
		"Underfitting misses structure; overfitting learns training-specific noise.",
		"Leakage occurs whenever training receives information unavailable at real prediction time.",
	],
	"Linear Regression": [
		"Ordinary least squares chooses coefficients that minimize the sum of squared residuals.",
		"Closed-form solvers and gradient descent optimize the same objective through different procedures.",
		"Check linearity, residual independence, roughly constant variance, and influential outliers.",
		"Compare with a mean baseline; Ridge shrinks coefficients and Lasso can set some to zero.",
	],
	"Classification and Model Evaluation": [
		"Logistic regression converts a linear score into a probability with the sigmoid function.",
		"Changing the threshold trades false positives against false negatives without retraining.",
		"Accuracy can hide failure on a rare class; precision and recall expose different error costs.",
		"Use MAE/RMSE/R² for regression and confusion-derived metrics for classification.",
	],
	"Neural Networks and PyTorch": [
		"Without nonlinear activations, stacked linear layers collapse into one linear transformation.",
		"`loss.backward()` calculates gradients; the optimizer uses them to update parameters.",
		"Mini-batches trade noisy gradient estimates for memory and computation efficiency.",
		"`model.eval()` and inference mode make validation behavior stable and avoid gradient storage.",
	],
	"Reliable Machine-Learning Pipelines": [
		"Fit imputation, scaling, and encoding inside each training fold to prevent leakage.",
		"Cross-validation reports variation across folds, not one deceptively precise score.",
		"Select hyperparameters using validation evidence and evaluate once on the untouched test set.",
		"Persist preprocessing, model, schema, versions, parameters, metrics, and data identity together.",
	],
	"Serving and Deploying Models": [
		"Validate request fields before inference and return structured 4xx errors for invalid client input.",
		"Package the same fitted preprocessing pipeline used during training to prevent serving skew.",
		"Use immutable container tags or digests, scoped IAM roles, and secrets outside source code.",
		"Deploy behind a health check with logs, budgets, resource limits, and documented rollback.",
	],
	"Large Language Model Fundamentals": [
		"Text becomes token IDs, then vectors; the model predicts a distribution for the next token.",
		"Softmax probabilities come from relative logits and always sum to one.",
		"Temperature changes sampling sharpness but does not add knowledge or factual verification.",
		"Base models continue text; instruction models are adapted to follow task-oriented conversations.",
	],
	"Prompt Engineering and Structured Outputs": [
		"Separate trusted instructions from untrusted user content and retrieved documents.",
		"Examples demonstrate behavior, but diverse tests determine whether the behavior generalizes.",
		"Validate model output against a schema before storing it or passing it downstream.",
		"Treat every tool call as an untrusted proposal requiring authorization and argument validation.",
	],
	"Engineering LLM Applications": [
		"Normalize provider differences behind an application-owned interface and capability checks.",
		"Retry only transient errors with exponential backoff, jitter, and a total attempt limit.",
		"Trace model, prompt version, tool calls, tokens, latency, errors, and cost for every request.",
		"MCP tools perform actions while resources expose context; both require least-privilege access.",
	],
	"Retrieval-Augmented Generation": [
		"Chunk around meaningful document structure and retain source, page, section, and access metadata.",
		"Embed both chunks and queries into the same vector space before similarity comparison.",
		"Retrieval selects evidence; generation must remain constrained to that supplied evidence.",
		"Refuse or state insufficient evidence when no retrieved passage supports an answer.",
	],
	"RAG Quality and LLM Evaluation": [
		"Evaluate ingestion, retrieval, context assembly, and generation as separate failure boundaries.",
		"Hybrid retrieval combines exact-term and semantic strengths without directly adding unlike scores.",
		"Rerank only a small candidate set to improve quality while controlling latency and cost.",
		"Calibrate automated judges against human ratings and inspect disagreements rather than hiding them.",
	],
	"AI Agents and LangGraph Workflows": [
		"Use deterministic workflows when steps are known; grant an agent choice only where it adds value.",
		"Typed state makes every node input, output, and routing decision inspectable.",
		"Tools need schemas, authorization, timeouts, resource limits, and observable results.",
		"Bound total steps and attempts, checkpoint recoverable state, and route uncertainty to a human.",
	],
	"Production AI Capstone": [
		"Translate the user need into measurable quality, safety, latency, and cost acceptance criteria.",
		"Draw data flow and trust boundaries before selecting frameworks or implementation details.",
		"Demonstrate unsupported, malformed, denied, timeout, and insufficient-evidence cases.",
		"Release with versioned artifacts, monitoring, budget alerts, runbook, limitations, and rollback.",
	],
}

for lesson in LESSONS:
	lesson["deepening"] = DEEPENING[lesson["title"]]


WEEKS = [week(number, lesson) for number, lesson in enumerate(LESSONS, start=1)]
MODULES = WEEKS
