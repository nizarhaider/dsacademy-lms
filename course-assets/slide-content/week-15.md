# Week 15: Retrieval-Augmented Generation

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who can build validated LLM calls and understand embeddings  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 15 presentation and related media.

---

## Slide 1 - RAG Supplies Evidence at Request Time

### Teaching purpose

Define retrieval-augmented generation and its boundaries.

### Learner-facing content

**Retrieval-augmented generation (RAG)** finds relevant evidence and includes it in the model context before generation.

The two main phases are:

- **ingestion:** parse, clean, chunk, embed, and index documents;
- **query:** retrieve chunks, assemble context, generate, validate, and cite.

RAG can use current or private documents without changing model weights. It does not guarantee that retrieval found the right evidence or that generation used it faithfully.

### Worked example

Question: `What is the refund period?`

Retriever returns a policy chunk stating `Refund requests are accepted within 14 days.` The model answers `14 days` and cites the source section.

Without supporting text, the system should return insufficient evidence.

### Code example

```text
question -> retrieve evidence -> build context -> generate answer -> verify citations
```

Expected output:

```text
An answer supported by retrieved chunks or an explicit insufficient-evidence result.
```

### Visual description

Separate ingestion and query pipelines meet at a vector index; citations point back to source documents.

### Instructor notes

Ask which failure belongs to retrieval and which belongs to generation.

### Notebook connection

The from-scratch notebook builds each RAG stage explicitly before using a framework.

### Sources

- [AI Bootcamp: RAG from Scratch](https://github.com/curiousily/AI-Bootcamp/blob/master/17.rag-from-scratch.ipynb)
- [AI Bootcamp: Build RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/06.build-rag.ipynb)

---

## Slide 2 - Parsing Recovers Content from Source Files

### Teaching purpose

Explain document parsing and extraction failure.

### Learner-facing content

**Document parsing** converts a source format into structured text and metadata.

A parser may need to recover:

- headings and paragraphs;
- tables;
- page numbers;
- lists and reading order;
- captions;
- document identifiers.

PDF is designed for visual layout, so extracted text may have broken order, missing tables, or repeated headers. Ingestion must inspect output rather than assuming successful file opening means correct extraction.

### Worked example

Two-column PDF text may be extracted across columns:

`left line 1, right line 1, left line 2...`

The words exist, but reading order is corrupted. A retrieval result from that text may be misleading.

### Code example

```python
documents = parser.load("policy.pdf")
print(len(documents), documents[0].metadata)
```

Expected output:

```text
Extracted document units plus source and page metadata for inspection.
```

### Visual description

A PDF page with headings, columns, and table becomes structured blocks; one broken extraction path is highlighted.

### Instructor notes

Require visual comparison between several extracted pages and the original file.

### Notebook connection

The advanced RAG notebook begins with document parsing before embeddings.

### Sources

- [LangChain: Document Loaders](https://docs.langchain.com/oss/python/integrations/document_loaders)
- [AI Bootcamp: Advanced RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/07.advanced-rag-with-llama-3-in-langchain.ipynb)

---

## Slide 3 - Cleaning Must Preserve Provenance

### Teaching purpose

Teach metadata and source traceability.

### Learner-facing content

**Cleaning** removes extraction noise or normalizes representation without changing meaning.

**Provenance** records where every block came from:

- source ID and version;
- page;
- section heading;
- stable URL or file path;
- ingestion time;
- access-control metadata.

Keep raw extracted text or a reference to it. If cleaning changes content, the transformation should be reproducible and inspectable.

### Worked example

Repeated header `DS Academy Policy 2026` appears on every page.

Removing exact repeated headers is reasonable. Removing every line containing `Policy` may delete real content. Record the cleaning rule and compare before/after counts.

### Code example

```python
chunk.metadata = {
    "source_id": "policy-2026-v3",
    "page": 7,
    "section": "Refunds",
}
```

Expected output:

```text
Each future retrieval result can identify its exact source location.
```

### Visual description

A cleaned text block remains linked by an unbroken provenance chain to source, page, section, and version.

### Instructor notes

Explain that citations cannot be reconstructed reliably if provenance was discarded during ingestion.

### Notebook connection

Learners add metadata before chunk storage, not after answering.

### Sources

- [LangChain: Documents](https://python.langchain.com/docs/concepts/documents/)
- [W3C PROV Overview](https://www.w3.org/TR/prov-overview/)

---

## Slide 4 - Chunking Defines the Unit of Retrieval

### Teaching purpose

Explain chunk size, boundaries, and overlap.

### Learner-facing content

A **chunk** is one retrievable evidence unit.

Chunking choices affect:

- whether a complete idea stays together;
- embedding specificity;
- retrieval recall;
- prompt size;
- citation precision.

**Overlap** repeats boundary text in adjacent chunks. It can preserve context but increases storage and duplicate retrieval.

Prefer document structure such as headings and paragraphs before fixed character cuts.

### Worked example

A 900-token section becomes:

- three chunks of 300 tokens with no overlap; or
- four chunks near 300 tokens with 50-token overlap.

The second keeps boundary context but may retrieve repeated statements.

### Code example

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)
chunks = splitter.split_documents(documents)
```

Expected output:

```text
A list of chunks retaining source metadata and bounded text lengths.
```

### Visual description

One section splits at paragraph boundaries; overlapping spans are shaded and duplicate context is marked.

### Instructor notes

Describe sizes as experiment settings, not universal recommendations.

### Notebook connection

Learners compare two chunking strategies on the same retrieval questions.

### Sources

- [LangChain: Text Splitters](https://docs.langchain.com/oss/python/integrations/splitters)
- [AI Bootcamp: RAG from Scratch](https://github.com/curiousily/AI-Bootcamp/blob/master/17.rag-from-scratch.ipynb)

---

## Slide 5 - Embeddings Place Chunks and Queries in One Vector Space

### Teaching purpose

Connect Week 12 embeddings to semantic retrieval.

### Learner-facing content

An **embedding model** maps text into a fixed-length vector.

For vector retrieval:

1. embed every document chunk;
2. store chunk vector plus text and metadata;
3. embed the user query with the same compatible model;
4. compare the query vector with chunk vectors;
5. return the highest-ranked allowed chunks.

Changing embedding model usually requires rebuilding the stored index.

### Worked example

Three chunks become 768-dimensional vectors. The query also becomes a 768-dimensional vector.

The shapes match, allowing similarity comparison. A 384-dimensional query from another model cannot be compared directly.

### Code example

```python
chunk_vectors = embedder.embed_documents(chunk_texts)
query_vector = embedder.embed_query(question)
print(len(chunk_vectors[0]), len(query_vector))
```

Expected output:

```text
Matching embedding dimensions.
```

### Visual description

Chunks and query enter the same embedding model and appear as points in one vector space.

### Instructor notes

Explain that “semantic” similarity reflects model training and may fail on identifiers, numbers, or domain language.

### Notebook connection

Both RAG notebooks create document and query embeddings before search.

### Sources

- [LangChain: Embedding Models](https://docs.langchain.com/oss/python/integrations/text_embedding)
- [AI Bootcamp: Build RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/06.build-rag.ipynb)

---

## Slide 6 - Cosine Similarity Compares Vector Direction

### Teaching purpose

Explain the retrieval equation with a small numerical example.

### Learner-facing content

Cosine similarity:

`cos(a,b) = (a · b) / (||a|| ||b||)`

- `a · b`: dot product
- `||a||`: length of vector `a`
- denominator normalizes vector magnitudes
- result is commonly between `-1` and `1`

Higher cosine similarity means vector directions are more aligned. Whether higher means more relevant must be tested for the task.

### Worked example

`a=[1,0]`, `b=[1,1]`

Dot product `= 1`  
`||a|| = 1`  
`||b|| = sqrt(2)`  
Cosine `= 1/sqrt(2) ≈ 0.707`

### Code example

```python
import numpy as np

a = np.array([1.0, 0.0])
b = np.array([1.0, 1.0])
similarity = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
print(round(similarity, 3))
```

Expected output:

```text
0.707
```

### Visual description

Two arrows form a 45-degree angle; dot product, lengths, and cosine calculation appear beside them.

### Instructor notes

Explain that database APIs may return distance rather than similarity, so score direction must be checked.

### Notebook connection

The from-scratch notebook calculates similarity before relying on a vector database.

### Sources

- [Scikit-learn: cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [AI Bootcamp: RAG from Scratch](https://github.com/curiousily/AI-Bootcamp/blob/master/17.rag-from-scratch.ipynb)

---

## Slide 7 - A Vector Store Connects Vectors to Evidence

### Teaching purpose

Define storage, indexing, metadata filtering, and tenant isolation.

### Learner-facing content

A **vector store** keeps:

- embedding vector;
- chunk text or reference;
- source metadata;
- access metadata;
- stable chunk ID.

An exact search compares all vectors. Approximate indexes trade some recall for lower latency at scale.

Apply authorization filters before or during retrieval. Filtering after retrieval can leak whether protected documents exist and waste candidate slots.

### Worked example

User belongs to tenant `A`.

Search condition:

`tenant_id = A AND document_status = published`

Only vectors satisfying both conditions may compete for top-k ranking.

### Code example

```python
results = vector_store.similarity_search(
    question,
    k=5,
    filter={"tenant_id": tenant_id, "status": "published"},
)
```

Expected output:

```text
Up to five authorized chunks with text, score, and provenance.
```

### Visual description

An index contains multiple tenants; an authorization filter creates a permitted subset before ranking.

### Instructor notes

Treat access control as a retrieval requirement, not a prompt instruction.

### Notebook connection

Learners store text and metadata together and test a denied cross-tenant query.

### Sources

- [LangChain: Vector Stores](https://docs.langchain.com/oss/python/integrations/vectorstores)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

---

## Slide 8 - Retrieval Selects Top-k Evidence

### Teaching purpose

Explain ranking, top-k, and evidence insufficiency.

### Learner-facing content

A **retriever** turns a question into an ordered list of chunks.

`top-k` is the maximum number returned.

Larger `k` may improve coverage but adds irrelevant or duplicated context. Smaller `k` is focused but may miss necessary evidence.

Inspect:

- query;
- returned text;
- scores and score direction;
- source diversity;
- metadata filters;
- whether the answer requires multiple chunks.

### Worked example

Relevant policy appears at rank `4`.

With `k=3`, it is missed.  
With `k=5`, it is included alongside two irrelevant chunks.

The choice must be evaluated across a query dataset, not one example.

### Code example

```python
for rank, document in enumerate(retriever.invoke(question), start=1):
    print(rank, document.metadata, document.page_content[:120])
```

Expected output:

```text
An inspectable ranked list with source metadata and text previews.
```

### Visual description

A ranked result list shows relevant, irrelevant, and duplicate chunks under different k cutoffs.

### Instructor notes

Require learners to evaluate retrieval before reading the generated answer.

### Notebook connection

The notebook's nearest-neighbour results become an explicit retrieval report.

### Sources

- [LangChain: Retrievers](https://python.langchain.com/docs/concepts/retrievers/)
- [AI Bootcamp: RAG from Scratch](https://github.com/curiousily/AI-Bootcamp/blob/master/17.rag-from-scratch.ipynb)

---

## Slide 9 - Context Assembly Builds the Evidence Packet

### Teaching purpose

Explain ordering, deduplication, labels, and budget control.

### Learner-facing content

**Context assembly** converts retrieved chunks into a model-ready evidence packet.

It should:

- remove duplicates;
- preserve source IDs and locations;
- order chunks deliberately;
- separate evidence from instructions;
- trim to the token budget;
- include only authorized content;
- avoid splitting a citation from its text.

The model should be told that retrieved content is untrusted evidence, not new instructions.

### Worked example

Five chunks consume `3,200` tokens, but evidence budget is `2,000`.

After deduplication, four chunks consume `2,500`. The assembler selects the highest-value set under `2,000` while retaining at least one chunk from each required source.

### Code example

```python
context = "\n\n".join(
    f"[{doc.metadata['source_id']} p.{doc.metadata['page']}]\n{doc.page_content}"
    for doc in selected_docs
)
```

Expected output:

```text
A labelled context packet whose citations can map back to retrieved documents.
```

### Visual description

Ranked chunks pass through deduplicate, authorize, budget, label, and order stages.

### Instructor notes

Explain why simply joining all top-k text can overweight duplicates and exceed context limits.

### Notebook connection

Learners build context explicitly before the generation call.

### Sources

- [LangChain: RAG Tutorial](https://docs.langchain.com/oss/python/langchain/rag)
- [AI Bootcamp: Build RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/06.build-rag.ipynb)

---

## Slide 10 - Grounded Answers Need Verifiable Citations

### Teaching purpose

Define grounded generation and citation validation.

### Learner-facing content

An answer is **grounded** when its factual claims are supported by the supplied evidence.

A **citation** identifies the exact source and location supporting a claim.

Validation should check:

- cited source was retrieved;
- cited passage supports the nearby claim;
- no unsupported claims were added;
- quotation and numbers match;
- insufficient evidence produces refusal or qualification.

A citation string generated by the model is not proof by itself.

### Worked example

Evidence: `[policy-v3 p.7] Refund requests are accepted within 14 days.`

Supported answer: `Refund requests are accepted within 14 days [policy-v3 p.7].`

Unsupported addition: `A full refund is guaranteed.` The passage does not support that claim.

### Code example

```python
valid_ids = {doc.metadata["chunk_id"] for doc in selected_docs}
assert set(answer.citation_ids) <= valid_ids
```

Expected output:

```text
The citation-ID check passes only for chunks actually supplied to the model.
```

### Visual description

Each answer claim connects to a supporting passage. One unsupported claim has no connection and is rejected.

### Instructor notes

Citation existence and citation support are separate checks.

### Notebook connection

Learners add stable chunk IDs to the answer schema and verify them.

### Sources

- [LangSmith: Evaluate RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)
- [AI Bootcamp: Build RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/06.build-rag.ipynb)

---

## Slide 11 - A RAG Failure Has an Owning Stage

### Teaching purpose

Teach stage-by-stage diagnosis.

### Learner-facing content

Common failure boundaries:

- parsing lost text;
- cleaning changed meaning;
- chunk boundary split evidence;
- embedding failed on domain terms;
- filter excluded the source;
- top-k missed the relevant chunk;
- context assembly removed or duplicated evidence;
- generator ignored evidence;
- citation did not support the claim.

Fix the owning stage. Prompt changes cannot restore text that ingestion lost.

### Worked example

Answer misses the refund period.

Diagnosis:

1. source PDF contains `14 days`;
2. parsed text contains it;
3. chunk index contains it;
4. retriever ranks it `12`;
5. top-k is `5`.

Owning failure is retrieval ranking, not generation.

### Code example

```python
debug_record = {
    "query": question,
    "retrieved_chunk_ids": [d.metadata["chunk_id"] for d in docs],
    "answer": answer.model_dump(),
}
```

Expected output:

```text
One trace connecting query, evidence, answer, and citations.
```

### Visual description

The RAG pipeline has diagnostic checkpoints; a failure marker sits at retrieval rank.

### Instructor notes

Ask learners to prove every upstream stage before changing the model prompt.

### Notebook connection

The lab records intermediate artifacts for each query.

### Sources

- [LangSmith: Evaluation Concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [LangSmith: Evaluate RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)

---

## Slide 12 - Guided Lab: Build RAG from Scratch

### Teaching purpose

Set a complete, inspectable RAG exercise.

### Learner-facing content

Build a small policy assistant:

1. parse and visually verify source pages;
2. preserve source, page, section, and access metadata;
3. compare two chunking strategies;
4. embed chunks and queries with one model;
5. calculate one cosine similarity by hand;
6. store vectors and metadata;
7. retrieve authorized top-k chunks;
8. inspect ranks before generation;
9. assemble deduplicated labelled context;
10. return structured answer and citation IDs;
11. verify citation support;
12. refuse an unsupported question.

### Worked example

Required test:

Question whose answer exists, question requiring two chunks, exact identifier query, unsupported question, and unauthorized-document query.

Each failure must identify its owning stage.

### Code example

```python
answer = rag(question, user_context)
assert all(cid in retrieved_ids for cid in answer.citation_ids)
```

Expected output:

```text
A grounded answer with valid citations or a typed insufficient/denied result.
```

### Visual description

An end-to-end lab checklist spans source verification through citation support and refusal.

### Instructor notes

Require retrieval inspection before judging answer quality. Do not hide the mechanism behind a framework-only call.

### Notebook connection

Complete `17.rag-from-scratch.ipynb` and `06.build-rag.ipynb`.

### Sources

- [AI Bootcamp: RAG from Scratch](https://github.com/curiousily/AI-Bootcamp/blob/master/17.rag-from-scratch.ipynb)
- [AI Bootcamp: Build RAG](https://github.com/curiousily/AI-Bootcamp/blob/master/06.build-rag.ipynb)
