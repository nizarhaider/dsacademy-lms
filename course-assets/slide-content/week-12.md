# Week 12: Large Language Model Fundamentals

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who understand tensors, probabilities, and deployed inference  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 12 presentation and related media.

---

## Slide 1 - A Language Model Predicts the Next Token

### Teaching purpose

Define an LLM by its training objective rather than its chat interface.

### Learner-facing content

A **language model** assigns probabilities to possible token sequences.

An autoregressive large language model repeatedly predicts:

`P(next token | tokens already in context)`

Generation is a loop:

1. tokenize the input;
2. calculate next-token scores;
3. convert scores to probabilities;
4. choose one token;
5. append it to context;
6. repeat until a stopping condition.

The model does not retrieve truth automatically. It predicts plausible continuations from learned parameters and supplied context.

### Worked example

Context: `The capital of Sri Lanka is`

Candidate probabilities might include:

`Colombo 0.55`, `Sri 0.12`, `Kandy 0.08`, others `0.25`.

The selected token is appended and the model predicts again.

### Code example

```python
prompt = "The capital of Sri Lanka is"
outputs = model.generate(**tokenizer(prompt, return_tensors="pt"), max_new_tokens=5)
```

Expected output:

```text
A sequence containing the prompt tokens followed by generated tokens.
```

### Visual description

A generation loop shows context, probability distribution, selected token, appended context, and repeat.

### Instructor notes

Separate fluent prediction from verified knowledge. Use “token” rather than “word” until tokenization is explained.

### Notebook connection

The LLMs 101 notebook performs a simple next-token prediction before chat generation.

### Sources

- [Hugging Face: Text Generation](https://huggingface.co/docs/transformers/main_classes/text_generation)
- [AI Bootcamp: LLMs 101](https://github.com/curiousily/AI-Bootcamp/blob/master/05.llms-101.ipynb)

---

## Slide 2 - Tokenization Converts Text into IDs

### Teaching purpose

Explain the model's discrete input representation.

### Learner-facing content

A **tokenizer** converts text into tokens and integer **token IDs** from a fixed vocabulary.

A token may be:

- a complete word;
- part of a word;
- punctuation;
- whitespace pattern;
- special control marker.

Tokenization depends on the model. Character count and word count do not equal token count.

The decoder maps token IDs back to text, but decoding individual tokens can look unusual because boundaries and spaces are encoded.

### Worked example

The word `unhelpful` might become pieces such as:

`un` + `help` + `ful`

If these map to IDs `[320, 912, 77]`, the model receives numbers, not raw letters.

### Code example

```python
encoded = tokenizer("Data science", add_special_tokens=False)
print(encoded["input_ids"])
print(tokenizer.convert_ids_to_tokens(encoded["input_ids"]))
```

Expected output:

```text
A model-specific list of token IDs and token strings.
```

### Visual description

Text splits into token pieces, each maps to an ID, then IDs form an input sequence.

### Instructor notes

Run the same text through only the notebook's tokenizer; exact tokens vary across models.

### Notebook connection

The notebook inspects token IDs and decodes generated sequences.

### Sources

- [Hugging Face: Tokenizer Summary](https://huggingface.co/docs/transformers/tokenizer_summary)
- [AI Bootcamp: LLMs 101](https://github.com/curiousily/AI-Bootcamp/blob/master/05.llms-101.ipynb)

---

## Slide 3 - Embeddings Turn Token IDs into Vectors

### Teaching purpose

Connect discrete tokens to neural-network representations.

### Learner-facing content

An **embedding** maps a token ID to a learned vector.

If hidden size is `d`, each token begins as a vector with `d` numerical components. The model also needs position information because token order changes meaning.

During transformer layers, representations become **contextual**: the vector for a token changes according to surrounding tokens.

Embedding similarity can reflect learned usage patterns, but it does not guarantee factual or logical equivalence.

### Worked example

Sequence length `6`, hidden size `4`.

Token-ID shape: `(6,)`  
Embedding shape: `(6,4)`

There is one four-number vector per token.

### Code example

```python
input_ids = torch.tensor([[10, 20, 30]])
embeddings = model.get_input_embeddings()(input_ids)
print(embeddings.shape)
```

Expected output:

```text
torch.Size([1, 3, hidden_size])
```

### Visual description

Three token IDs each expand into a vector row, forming a sequence-by-hidden-size matrix.

### Instructor notes

Do not present individual vector dimensions as human-readable concepts.

### Notebook connection

RAG later uses separate embedding models to represent document chunks and queries.

### Sources

- [Hugging Face: Model Outputs](https://huggingface.co/docs/transformers/main_classes/output)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

---

## Slide 4 - Self-Attention Mixes Information Across Tokens

### Teaching purpose

Give a conceptual transformer mechanism without excessive matrix detail.

### Learner-facing content

A **transformer** processes token representations with repeated attention and feed-forward blocks.

In **self-attention**, each token:

1. forms a query describing what information it seeks;
2. compares that query with keys from allowed tokens;
3. converts comparisons into attention weights;
4. combines value vectors using those weights.

In causal generation, a token cannot attend to future tokens that have not been generated.

### Worked example

Sentence: `The bank raised its rate because it expected inflation.`

When representing the second `it`, attention may assign more weight to `bank` and surrounding context. The result is a context-dependent representation.

### Code example

```text
attention(Q, K, V) = softmax(QK^T / sqrt(dk)) V
```

Expected output:

```text
One context-mixed vector per token for each attention head.
```

### Visual description

One token sends weighted lines to earlier tokens, then combines their value vectors. Future positions are masked.

### Instructor notes

Define query, key, and value by role, not as database concepts. Avoid claiming attention weights are complete explanations.

### Notebook connection

The notebook uses a pretrained transformer; learners now understand its core data flow.

### Sources

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Hugging Face: Causal Language Modeling](https://huggingface.co/docs/transformers/tasks/language_modeling)

---

## Slide 5 - The Context Window Is a Finite Token Budget

### Teaching purpose

Explain what fits into one model call.

### Learner-facing content

The **context window** is the maximum token sequence the model can process in one request, including some combination of:

- system and user messages;
- conversation history;
- retrieved documents;
- tool results;
- generated output.

Longer context consumes memory, latency, and cost. Content may be truncated or rejected when the limit is exceeded.

More context is not always better: irrelevant or conflicting text can reduce answer quality.

### Worked example

Context limit `8,000` tokens.

Instructions `500`  
History `2,000`  
Retrieved evidence `3,500`  
Reserved output `1,000`

Total `7,000`, leaving `1,000` tokens of headroom.

### Code example

```python
token_count = len(tokenizer(prompt)["input_ids"])
print(token_count)
```

Expected output:

```text
The model-specific number of input tokens.
```

### Visual description

A fixed-width context bar allocates tokens to instructions, history, evidence, and output.

### Instructor notes

Explain why character truncation can split tokens and why output budget must be reserved.

### Notebook connection

Learners should inspect prompt token counts before generation.

### Sources

- [Hugging Face: Generation Parameters](https://huggingface.co/docs/transformers/main_classes/text_generation)
- [AI Bootcamp: LLMs 101](https://github.com/curiousily/AI-Bootcamp/blob/master/05.llms-101.ipynb)

---

## Slide 6 - Logits Become Probabilities through Softmax

### Teaching purpose

Explain next-token scoring with a complete numerical example.

### Learner-facing content

For each vocabulary token, the model produces a **logit**: an unrestricted score.

Softmax converts logits into probabilities:

`P(i) = e^(zi) / Σj e^(zj)`

- `zi`: logit for token `i`
- exponentials make values positive
- denominator adds exponentials for all candidates
- probabilities sum to `1`

Only relative logit differences matter.

### Worked example

Logits `[2,1,0]`

Exponentials approximately `[7.39,2.72,1.00]`  
Sum `11.11`

Probabilities:

`[7.39/11.11, 2.72/11.11, 1/11.11]`  
`≈ [0.665,0.245,0.090]`

### Code example

```python
logits = torch.tensor([2.0, 1.0, 0.0])
print(torch.softmax(logits, dim=0))
```

Expected output:

```text
tensor([0.6652, 0.2447, 0.0900])
```

### Visual description

Three raw logits pass through exponentiation, normalization, and a probability bar chart.

### Instructor notes

Calculate each step. Explain that logits are not percentages.

### Notebook connection

The notebook inspects model logits and selects likely next tokens.

### Sources

- [PyTorch: softmax](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.softmax.html)
- [Hugging Face: Generation Scores](https://huggingface.co/docs/transformers/main_classes/text_generation)

---

## Slide 7 - Sampling Controls How a Token Is Chosen

### Teaching purpose

Separate probability estimation from decoding strategy.

### Learner-facing content

**Greedy decoding** selects the highest-probability token each step.

**Sampling** randomly selects according to a probability distribution.

**Temperature** rescales logits before softmax:

`softmax(logits / T)`

- lower `T` sharpens the distribution;
- higher `T` flattens it;
- temperature does not add knowledge or verify facts.

Top-k and top-p restrict which candidates may be sampled.

### Worked example

At low temperature, probabilities might be `[0.90,0.08,0.02]`.  
At higher temperature, they might be `[0.55,0.30,0.15]`.

The first remains most likely, but alternatives are selected more often.

### Code example

```python
outputs = model.generate(
    **inputs,
    do_sample=True,
    temperature=0.7,
    max_new_tokens=40,
)
```

Expected output:

```text
One sampled continuation whose exact wording can differ between runs.
```

### Visual description

The same logits produce sharp and flat probability bars under two temperatures, then a sampling wheel.

### Instructor notes

Do not call low temperature deterministic when sampling is still enabled. Use a seed only for controlled demonstrations.

### Notebook connection

Learners compare greedy and sampled generation while keeping the prompt fixed.

### Sources

- [Hugging Face: Generation Strategies](https://huggingface.co/docs/transformers/generation_strategies)
- [Hugging Face: GenerationConfig](https://huggingface.co/docs/transformers/main_classes/text_generation)

---

## Slide 8 - Base and Instruction Models Have Different Training Goals

### Teaching purpose

Explain why the same prompt behaves differently across model variants.

### Learner-facing content

A **base model** is pretrained mainly to continue token sequences.

An **instruction model** is further adapted using instruction-response examples and often preference training so it follows conversational tasks more reliably.

Instruction models usually expect a model-specific **chat template** containing role and control tokens. Sending plain text to an instruction model or chat-formatted text to a base model changes behaviour.

Neither model type guarantees truth, safety, or task correctness.

### Worked example

Prompt to a base model:

`Question: What is 2+2? Answer:`

may continue a learned document pattern.

An instruction model receives structured messages such as user request and assistant turn, then generates the assistant response.

### Code example

```python
messages = [{"role": "user", "content": "Explain tokenization simply."}]
prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
```

Expected output:

```text
A model-specific text prompt containing the required chat control tokens.
```

### Visual description

Base pretraining and instruction adaptation form two branches with different expected prompt formats.

### Instructor notes

Do not describe instruction tuning as adding current knowledge. It primarily changes task-following behaviour.

### Notebook connection

The LLMs 101 notebook loads both base and instruction-tuned variants.

### Sources

- [Hugging Face: Chat Templates](https://huggingface.co/docs/transformers/chat_templating)
- [AI Bootcamp: LLMs 101](https://github.com/curiousily/AI-Bootcamp/blob/master/05.llms-101.ipynb)

---

## Slide 9 - Hallucination Is Unsupported Generation

### Teaching purpose

Define failure in evidence terms and set safe application expectations.

### Learner-facing content

A **hallucination** is generated content presented as factual despite lacking support or being incorrect.

LLMs can:

- invent citations;
- combine incompatible facts;
- follow false assumptions in a prompt;
- produce outdated information;
- make arithmetic or logical mistakes;
- sound confident while uncertain.

Mitigations include trusted retrieval, tools, structured validation, explicit refusal rules, test datasets, and human review. A prompt alone cannot guarantee factuality.

### Worked example

Question asks for a policy section that does not exist in the supplied document.

Unsafe answer invents a section number.  
Grounded answer states that the evidence does not contain the requested policy and cites what was checked.

### Code example

```python
if not supporting_chunks:
    return {"answer": None, "reason": "insufficient_evidence"}
```

Expected output:

```text
A machine-readable refusal instead of an unsupported factual answer.
```

### Visual description

One generation path invents a claim; another checks evidence and returns an explicit insufficient-evidence result.

### Instructor notes

Use “unsupported” as an observable criterion. Avoid implying that confidence wording reveals true model certainty.

### Notebook connection

Later RAG lessons add evidence retrieval and citation checks around generation.

### Sources

- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/itl/ai-risk-management-framework)
- [Hugging Face: LLM Course](https://huggingface.co/learn/llm-course/)

---

## Slide 10 - Quantization Trades Precision for Resource Use

### Teaching purpose

Explain how local model inference can fit smaller hardware.

### Learner-facing content

**Quantization** stores or computes model values with lower numerical precision.

Possible effects:

- lower memory use;
- faster inference on supported hardware;
- smaller model files;
- some quality loss;
- hardware- and implementation-dependent speed.

Quantization does not reduce prompt tokens or expand the context window automatically. Evaluate the quantized model on the actual tasks before deployment.

### Worked example

One billion parameters:

- 16-bit storage is roughly `2 GB` for raw weights;
- 8-bit storage is roughly `1 GB`;
- 4-bit storage is roughly `0.5 GB`.

Runtime requires additional memory for cache and application state.

### Code example

```text
Approximate raw weight bytes = parameter_count x bits_per_parameter / 8
```

Expected output:

```text
1,000,000,000 x 4 / 8 = approximately 500,000,000 bytes.
```

### Visual description

The same model appears as 16-bit, 8-bit, and 4-bit weight blocks with decreasing size and an evaluation warning.

### Instructor notes

Describe estimates as raw-weight approximations, not total runtime memory.

### Notebook connection

Ollama commonly runs quantized local models; learners should inspect the selected model size.

### Sources

- [Hugging Face: Quantization](https://huggingface.co/docs/transformers/quantization/overview)
- [Ollama: Model Import](https://docs.ollama.com/import)

---

## Slide 11 - Ollama Provides a Local Model Runtime

### Teaching purpose

Connect model fundamentals to a practical local inference service.

### Learner-facing content

Ollama runs supported models locally and exposes a command-line and HTTP interface.

Key ideas:

- model identifier and version determine the artifact;
- local runtime still consumes CPU, memory, and storage;
- prompts and responses remain on the machine unless the application sends data elsewhere;
- local does not automatically mean secure;
- output must still be validated and evaluated.

Use only model licences and sizes suitable for the intended environment.

### Worked example

Workflow:

1. pull a small model;
2. run one prompt;
3. inspect token and latency behaviour;
4. call the local API;
5. stop the model when not needed.

### Code example

```bash
ollama run <model-name> "Explain what a token is in one sentence."
```

Expected output:

```text
A locally generated response from the selected installed model.
```

### Visual description

A laptop contains the Ollama runtime and model, with CLI and local HTTP clients connecting to it.

### Instructor notes

Do not hardcode a model name in the lesson; available models and licences change. Record the exact selected artifact in the lab.

### Notebook connection

The Ollama quickstart notebook introduces local generation after the model mechanism is understood.

### Sources

- [Ollama Documentation](https://docs.ollama.com/)
- [AI Bootcamp: Ollama Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/28.ollama-quickstart.ipynb)

---

## Slide 12 - Guided Lab: Trace One Generated Token

### Teaching purpose

Set a mechanism-focused LLM practical.

### Learner-facing content

Complete:

1. tokenize a short prompt and inspect IDs;
2. report input token count;
3. inspect model and tokenizer identifiers;
4. obtain next-token logits;
5. apply softmax to a small candidate set;
6. identify the highest-probability token;
7. compare greedy and sampled generation;
8. change temperature and describe the distribution change;
9. compare base and instruction prompt formats;
10. run a small local model with Ollama;
11. record latency and model size;
12. document one unsupported answer and a safer response.

### Worked example

For logits `[2,1,0]`, probabilities are approximately `[0.665,0.245,0.090]`. Greedy decoding chooses the first token; sampling may choose another.

### Code example

```python
next_logits = outputs.logits[0, -1]
top = torch.topk(torch.softmax(next_logits, dim=-1), k=5)
print(top.indices, top.values)
```

Expected output:

```text
Five model-specific token IDs and their next-token probabilities.
```

### Visual description

A trace sheet follows text, token IDs, embeddings, logits, probabilities, token choice, decoded text, and verification.

### Instructor notes

Require model-specific observations rather than memorized claims. Keep fine-tuning out of the core lab.

### Notebook connection

Complete `05.llms-101.ipynb` and `28.ollama-quickstart.ipynb`.

### Sources

- [AI Bootcamp: LLMs 101](https://github.com/curiousily/AI-Bootcamp/blob/master/05.llms-101.ipynb)
- [AI Bootcamp: Ollama Quickstart](https://github.com/curiousily/AI-Bootcamp/blob/master/28.ollama-quickstart.ipynb)
