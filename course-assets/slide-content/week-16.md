# Week 16: RAG Quality and LLM Evaluation

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who have built an inspectable RAG pipeline  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 16 presentation and related media.

---

## Slide 1 - Evaluate RAG as Separate Components

### Teaching purpose

Prevent one end-to-end score from hiding the owning failure.

### Learner-facing content

Evaluate at four boundaries:

1. **ingestion:** was source content recovered correctly?
2. **retrieval:** were relevant authorized chunks returned?
3. **context assembly:** was useful evidence preserved within budget?
4. **generation:** is the answer relevant, grounded, and correctly cited?

End-to-end correctness matters, but component metrics explain what to fix.

### Worked example

The answer is wrong because the required chunk ranked `8` and top-k was `5`.

Generation cannot use evidence it never received. The retrieval stage owns this failure even if the final answer is the visible symptom.

### Code example

```python
evaluation = {
    "retrieved_ids": retrieved_ids,
    "expected_ids": expected_ids,
    "answer": answer,
    "citation_ids": citation_ids,
}
```

Expected output:

```text
One evaluation record linking retrieval and answer evidence.
```

### Visual description

The RAG pipeline is divided into four independently scored sections.

### Instructor notes

Ask learners to identify the earliest stage where the expected evidence disappears.

### Notebook connection

The advanced RAG and evaluation notebooks provide candidate retrieval and generation experiments.

### Sources

- [LangSmith: Evaluate a RAG Application](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)
- [AI Bootcamp: LLM Evaluation](https://github.com/curiousily/AI-Bootcamp/blob/master/12.llm-evaluation.ipynb)

---

## Slide 2 - An Evaluation Dataset Represents Real Questions

### Teaching purpose

Define labelled queries and expected evidence.

### Learner-facing content

A RAG evaluation example should record:

- question;
- user or tenant context;
- expected relevant chunk IDs;
- reference answer or required facts when available;
- unsupported or denied expectation;
- importance and category;
- notes about ambiguity.

Include normal, rare, multi-chunk, exact-term, paraphrase, unsupported, and access-control cases.

### Worked example

Question: `How long do I have to request a refund?`

Expected chunk: `policy-v3-refunds-p7`  
Required fact: `14 days`  
Allowed outcome: supported answer with that citation  
Denied outcome: any answer using another tenant's policy

### Code example

```python
case = {
    "question": "How long do I have to request a refund?",
    "expected_chunk_ids": ["policy-v3-refunds-p7"],
    "required_facts": ["14 days"],
}
```

Expected output:

```text
A versioned test case with retrieval and answer expectations.
```

### Visual description

An evaluation dataset table includes categories, expected evidence, facts, and access context.

### Instructor notes

Begin with manually reviewed cases. Production logs can suggest new cases only after privacy review.

### Notebook connection

Learners construct a small fixed dataset before tuning retrieval parameters.

### Sources

- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [LangSmith: Evaluate RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)

---

## Slide 3 - Retrieval Precision and Recall Measure Different Goals

### Teaching purpose

Define retrieval metrics with a numerical example.

### Learner-facing content

For one query:

`retrieval precision = relevant retrieved / retrieved`

`retrieval recall = relevant retrieved / all relevant`

Precision asks how focused the results are. Recall asks how much required evidence was found.

The definition of relevant must come from labelled evidence, not from the retriever's own score.

### Worked example

Expected relevant chunks `{A,B,C}`.  
Retrieved chunks `{A,B,X,Y}`.

Relevant retrieved: `{A,B}` count `2`

Precision `= 2/4 = 0.50`  
Recall `= 2/3 = 0.667`

### Code example

```python
expected = {"A", "B", "C"}
retrieved = ["A", "B", "X", "Y"]
hits = expected.intersection(retrieved)
print(len(hits)/len(retrieved), len(hits)/len(expected))
```

Expected output:

```text
0.5 0.6666666666666666
```

### Visual description

Two overlapping sets show expected and retrieved chunks; equations use the intersection.

### Instructor notes

Explain that some questions require several chunks while others require only one.

### Notebook connection

Learners calculate precision and recall at several k values.

### Sources

- [Information Retrieval Evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html)
- [LangSmith: Evaluate RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)

---

## Slide 4 - Top-k and Filters Change the Candidate Set

### Teaching purpose

Teach controlled parameter experiments.

### Learner-facing content

`k` controls how many results enter the next stage.

Metadata filters can restrict:

- tenant or user access;
- document type;
- publication status;
- date;
- product or region.

Evaluate security filters as hard requirements. Tune relevance filters and k on the evaluation dataset, measuring quality, latency, token use, and duplicate rate.

### Worked example

At `k=3`: precision `0.67`, recall `0.50`  
At `k=8`: precision `0.38`, recall `1.00`

Higher k recovers all evidence but adds more irrelevant chunks. Reranking or better queries may improve the tradeoff.

### Code example

```python
for k in [3, 5, 8]:
    results = retrieve(query, k=k, filters=access_filter)
    record_metrics(k, results, expected)
```

Expected output:

```text
A comparable result row for each k under the same access filter and dataset.
```

### Visual description

Precision, recall, latency, and context tokens change across k values; access filtering remains fixed.

### Instructor notes

Never tune security boundaries for higher recall.

### Notebook connection

Learners run a small top-k experiment before changing models.

### Sources

- [LangChain: Retrievers](https://python.langchain.com/docs/concepts/retrievers/)
- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)

---

## Slide 5 - Query Rewriting Can Improve Retrieval

### Teaching purpose

Explain rewriting, expansion, and traceability.

### Learner-facing content

A **query rewrite** transforms a user's question into a search query.

Possible methods:

- resolve conversation references;
- expand abbreviations;
- generate alternate wording;
- split a multi-part question;
- add domain identifiers.

Rewriting can improve recall but may change intent. Preserve the original question and record every rewritten query.

### Worked example

Conversation:

User: `What is the refund period?`  
Later: `Does it apply to annual plans?`

Standalone rewrite:

`Does the 14-day refund period apply to annual plans?`

The rewrite should be checked against conversation state, not invented from unrelated context.

### Code example

```python
rewrite = rewrite_model.invoke({
    "history": history,
    "question": question,
})
trace["rewritten_query"] = rewrite
```

Expected output:

```text
A standalone search query recorded beside the original user question.
```

### Visual description

Original question and history enter a rewrite step; original and rewritten queries remain visible in the trace.

### Instructor notes

Evaluate whether rewrites preserve intent, not only whether retrieval scores rise.

### Notebook connection

Advanced RAG experiments can compare original and rewritten query retrieval.

### Sources

- [LangChain: Query Analysis](https://python.langchain.com/docs/tutorials/rag/#query-analysis)
- [AI Bootcamp: Advanced RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/07.advanced-rag-with-llama-3-in-langchain.ipynb)

---

## Slide 6 - Hybrid Search Combines Exact and Semantic Retrieval

### Teaching purpose

Explain lexical retrieval, vector retrieval, and rank fusion.

### Learner-facing content

Lexical search such as **BM25** is strong for exact terms, names, codes, and rare words.

Vector search is strong for semantic similarity and paraphrases.

**Hybrid search** combines candidate lists from both systems.

Raw lexical and vector scores have different meanings. **Reciprocal rank fusion (RRF)** combines ranks:

`RRF(d) = Σ 1 / (c + rank_i(d))`

### Worked example

Document A ranks `1` lexical and `4` vector.  
With `c=60`:

`1/61 + 1/64 ≈ 0.01639 + 0.01563 = 0.03202`

Documents found by both methods gain combined evidence.

### Code example

```python
def rrf_score(ranks, c=60):
    return sum(1 / (c + rank) for rank in ranks)
```

Expected output:

```text
A fusion score based on rank positions rather than incompatible raw scores.
```

### Visual description

Lexical and vector ranked lists merge through RRF into one fused order.

### Instructor notes

Do not claim hybrid always wins. Evaluate it on exact-term and paraphrase subsets.

### Notebook connection

Learners add a lexical candidate list before reranking.

### Sources

- [Elasticsearch: Reciprocal Rank Fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)
- [Stanford IR Book: Okapi BM25](https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html)

---

## Slide 7 - Reranking Applies a Stronger Model to Fewer Candidates

### Teaching purpose

Explain retrieve-many, rerank-few architecture.

### Learner-facing content

A **reranker** scores query-document pairs using a model more expensive than first-stage retrieval.

Pipeline:

1. retrieve a broader candidate set quickly;
2. rerank those candidates;
3. keep the best few for context.

Reranking can improve ordering but adds latency and cost. It cannot recover a relevant chunk missing from the candidate set.

### Worked example

Vector search retrieves `20` candidates. Relevant chunk ranks `11`.  
Reranker moves it to rank `2`.  
Final context keeps top `5`, so the evidence is now included.

If the chunk was not in the first `20`, reranking could not help.

### Code example

```python
candidates = retriever.invoke(query)[:20]
reranked = reranker.rerank(query, candidates)
context_docs = reranked[:5]
```

Expected output:

```text
Five final chunks selected from twenty first-stage candidates.
```

### Visual description

A wide candidate funnel narrows through a reranker into a focused context set.

### Instructor notes

Measure first-stage recall before blaming reranking.

### Notebook connection

The advanced RAG notebook includes a reranking stage before question answering.

### Sources

- [AI Bootcamp: Advanced RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/07.advanced-rag-with-llama-3-in-langchain.ipynb)
- [Sentence Transformers: Cross-Encoders](https://www.sbert.net/examples/cross_encoder/applications/README.html)

---

## Slide 8 - Answer Quality Has Several Dimensions

### Teaching purpose

Define correctness, relevance, groundedness, and citation support.

### Learner-facing content

- **Correctness:** agreement with a reference answer or verified facts
- **Relevance:** whether the response addresses the question
- **Groundedness:** whether claims are supported by supplied context
- **Citation correctness:** whether cited passages support nearby claims
- **Completeness:** whether required answer parts are present

An answer can be relevant but incorrect, correct by chance but ungrounded, or grounded but incomplete.

### Worked example

Question asks refund period and exclusions.

Answer gives `14 days` with support but omits annual-plan exclusions.

It may be grounded and partly correct, but incomplete.

### Code example

```python
scores = {
    "correctness": 1.0,
    "relevance": 1.0,
    "groundedness": 1.0,
    "completeness": 0.5,
}
```

Expected output:

```text
Separate dimensions reveal the omitted requirement.
```

### Visual description

One answer receives four independent gauges rather than one overall quality label.

### Instructor notes

Require a rubric for each dimension and examples of pass/fail boundaries.

### Notebook connection

The evaluation notebook builds metrics and a report across several answer dimensions.

### Sources

- [LangSmith: Evaluate RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)
- [AI Bootcamp: LLM Evaluation](https://github.com/curiousily/AI-Bootcamp/blob/master/12.llm-evaluation.ipynb)

---

## Slide 9 - Model Judges Need Human Calibration

### Teaching purpose

Explain LLM-as-judge benefits and risks.

### Learner-facing content

An **LLM judge** applies a rubric to an input, response, evidence, or reference answer.

Benefits:

- scalable evaluation of nuanced language;
- structured explanations;
- faster experiment comparison.

Risks:

- bias toward style or length;
- sensitivity to prompt and order;
- inconsistent scoring;
- shared errors with the evaluated model;
- cost and privacy concerns.

Calibrate judges against human-labelled examples and inspect disagreements.

### Worked example

On `50` examples, judge and human agree on `42`.

Agreement rate:

`42 / 50 = 0.84`

The `8` disagreements should be grouped by cause before trusting the judge at scale.

### Code example

```python
agreement = sum(j == h for j, h in zip(judge_labels, human_labels))
print(agreement / len(human_labels))
```

Expected output:

```text
0.84
```

### Visual description

Human and judge labels form an agreement matrix; disagreement examples feed rubric revision.

### Instructor notes

Do not treat model-judge scores as objective ground truth.

### Notebook connection

The evaluation notebook's critic model is compared with a manual rubric.

### Sources

- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [AI Bootcamp: LLM Evaluation](https://github.com/curiousily/AI-Bootcamp/blob/master/12.llm-evaluation.ipynb)

---

## Slide 10 - Failure Analysis Produces the Next Experiment

### Teaching purpose

Turn failed examples into actionable categories.

### Learner-facing content

For each failed query, record:

- source and parsing status;
- expected and retrieved chunks;
- ranks and filters;
- rewrite;
- context after assembly;
- answer and citations;
- metric and rubric failures;
- owning stage;
- proposed change.

Group failures such as exact-term miss, multi-chunk miss, duplicate context, unauthorized retrieval, unsupported claim, or incorrect citation.

### Worked example

Ten failed queries:

- 4 exact product codes missed by vector search;
- 3 relevant chunks ranked below k;
- 2 unsupported answers;
- 1 incorrect citation.

First experiment: add lexical retrieval for product-code cases, not rewrite every prompt.

### Code example

```python
failures.groupby(["owning_stage", "category"]).size()
```

Expected output:

```text
Counts showing which stage and failure type dominate.
```

### Visual description

Individual failures cluster into categories, which map to targeted experiments.

### Instructor notes

Require one change at a time so experiment effects remain attributable.

### Notebook connection

Learners build a failure report from evaluation traces.

### Sources

- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Slide 11 - An Experiment Report Includes Quality, Latency, and Cost

### Teaching purpose

Teach controlled comparison and release thresholds.

### Learner-facing content

Record for each RAG version:

- corpus and ingestion version;
- embedding model and index settings;
- retriever, filters, k, rewrite, and reranker;
- prompt and generation model;
- evaluation dataset version;
- component and end-to-end metrics;
- latency percentiles;
- input and output tokens;
- estimated cost;
- security failures;
- known limitations.

Do not release solely because one average improves.

### Worked example

Version B improves retrieval recall from `0.72` to `0.84`, but p95 latency rises from `1.2s` to `4.8s`.

If acceptance requires p95 under `2s`, Version B does not pass despite quality improvement.

### Code example

```python
accepted = (
    recall >= 0.80
    and groundedness >= 0.95
    and p95_latency_ms <= 2000
    and security_failures == 0
)
```

Expected output:

```text
True only when every release threshold passes.
```

### Visual description

A comparison table has quality, latency, cost, and security columns with explicit pass thresholds.

### Instructor notes

Separate hard constraints from optimization goals.

### Notebook connection

Learners produce one baseline and two controlled RAG experiment reports.

### Sources

- [LangSmith: Evaluation](https://docs.langchain.com/langsmith/evaluation)
- [LangSmith: Observability](https://docs.langchain.com/langsmith/observability)

---

## Slide 12 - Guided Lab: Improve RAG with Evidence

### Teaching purpose

Set the Week 16 quality-improvement exercise.

### Learner-facing content

Create at least `20` reviewed queries and:

1. label expected chunk IDs and required facts;
2. calculate retrieval precision and recall;
3. compare at least three k values;
4. test metadata filters;
5. compare original and rewritten queries;
6. add lexical retrieval and rank fusion;
7. rerank a fixed candidate set;
8. score correctness, relevance, groundedness, and citations;
9. calibrate one model judge with human labels;
10. classify every failure by owning stage;
11. compare latency, tokens, and cost;
12. choose a release candidate against explicit thresholds.

### Worked example

Do not accept “Version B feels better.” Report:

`recall +0.12`, `groundedness unchanged`, `p95 +3.6s`, `cost +40%`, and the decision based on requirements.

### Code example

```python
results = evaluate_versions(
    versions=[baseline, hybrid, reranked],
    dataset=test_cases,
)
print(results.groupby("version").mean(numeric_only=True))
```

Expected output:

```text
Comparable component and end-to-end metrics for each version.
```

### Visual description

An evaluation loop moves from dataset to component metrics, failure analysis, experiment, and release decision.

### Instructor notes

Lock the evaluation dataset before comparing versions and retain failed examples.

### Notebook connection

Complete `07.advanced-rag-with-llama-3-in-langchain.ipynb` and `12.llm-evaluation.ipynb`.

### Sources

- [AI Bootcamp: Advanced RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/07.advanced-rag-with-llama-3-in-langchain.ipynb)
- [AI Bootcamp: LLM Evaluation](https://github.com/curiousily/AI-Bootcamp/blob/master/12.llm-evaluation.ipynb)
