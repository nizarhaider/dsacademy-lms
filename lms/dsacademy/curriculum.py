"""Curriculum shared by LMS, slide, narration, and video generation."""

COURSE = {
	"title": "End-to-End Data Science & AI",
	"short_introduction": (
		"Build production-minded data products with Python, machine learning, "
		"generative AI, SQL, Spark, cloud deployment, and MLOps."
	),
	"description": """
<p>This 12-week flagship program moves from Python foundations to a deployed,
monitored capstone. Every week combines concepts, guided implementation,
independent practice, a knowledge check, and a portfolio-ready deliverable.</p>
<p>Learners can follow narrated explanations in English or Sinhala. The course
is designed for working professionals and university students who want an
applied, reproducible path into data science and AI engineering.</p>
""".strip(),
	"tags": "Python, Data Science, Machine Learning, Generative AI, SQL, Spark, MLOps",
}


def session(title, outcomes, concepts, lab, deliverable, narration_en, narration_si):
	return {
		"title": title,
		"outcomes": outcomes,
		"concepts": concepts,
		"lab": lab,
		"deliverable": deliverable,
		"narration_en": narration_en,
		"narration_si": narration_si,
	}


def week(title, focus, sessions, quiz, assignment):
	return {
		"title": title,
		"focus": focus,
		"sessions": sessions,
		"quiz": quiz,
		"assignment": assignment,
	}


WEEKS = [
	week(
		"Python Foundations for Data Work",
		"Write clear, testable Python and reason about data transformations.",
		[
			session(
				"Python for Data Science I",
				["Use core Python types and control flow intentionally.", "Write small functions with explicit inputs and outputs.", "Debug type, scope, and indexing errors."],
				["data types", "control flow", "functions", "exceptions"],
				"Build a reusable profiler for a list of transaction records.",
				"A tested Python module and concise debugging log.",
				"Python becomes useful for data work when every transformation is explicit. We move from collections to small testable functions and treat error messages as evidence.",
				"දත්ත සමඟ වැඩ කිරීමේදී සෑම පරිවර්තනයක්ම පැහැදිලිව ලිවීම වැදගත්ය. Collections සිට පහසුවෙන් පරීක්ෂා කළ හැකි කුඩා functions දක්වා යමු. Error message එකක් ගැටලුව සොයාගැනීමට ලැබෙන සාක්ෂියක් ලෙස භාවිත කරමු.",
			),
			session(
				"Python for Data Science II: NumPy",
				["Represent numerical data with arrays and meaningful shapes.", "Replace slow loops with vectorized operations.", "Explain broadcasting and shape mismatches."],
				["ndarrays", "indexing", "vectorization", "broadcasting"],
				"Calculate cohort retention and normalized scores from matrix data.",
				"A notebook comparing loop and vectorized implementations.",
				"NumPy gives numerical data a shape and makes whole-array operations concise. We inspect dimensions first, select with masks, and broadcast only when alignment is clear.",
				"NumPy මඟින් සංඛ්‍යාත්මක දත්තවල shape එක පැහැදිලි කර array එකක්ම එකවර සැකසිය හැක. Dimensions පරීක්ෂා කර boolean masks භාවිතයෙන් දත්ත තෝරමු. Alignment එක පැහැදිලි විට පමණක් broadcasting භාවිත කරමු.",
			),
		],
		[
			("Which construct best isolates a reusable transformation?", ["A function", "A comment", "A global variable", "A print statement"], 0),
			("What does an array shape describe?", ["Its dimensions", "Its file size", "Its color", "Its name"], 0),
			("Why is vectorization useful?", ["It expresses array operations efficiently", "It removes every error", "It encrypts data", "It creates labels"], 0),
		],
		("Transaction Quality Profiler", "Create a Python package that validates transaction records, reports invalid values, and computes three vectorized metrics.", "Correctness 40%, clarity 25%, tests 20%, explanation 15%."),
	),
	week(
		"Reproducible Projects, APIs & Data Apps",
		"Turn notebooks into maintainable projects that obtain and expose data.",
		[
			session(
				"Git and Reproducible Project Structure",
				["Use focused commits and branches.", "Separate source, tests, data, notebooks, and configuration.", "Recreate an environment from declared dependencies."],
				["Git history", "branching", "project layout", "environments"],
				"Refactor the week-one notebook into an installable repository.",
				"A repository with tests, a dependency lock, and meaningful commits.",
				"Reproducibility means rebuilding a result from code, data, and declared configuration. Git commits preserve decisions, while environments and project boundaries preserve execution.",
				"Reproducibility කියන්නේ code, data සහ configuration භාවිතයෙන් ප්‍රතිඵලය නැවත සාදාගත හැකි වීමයි. Git commits තීරණ සුරකින අතර environments සහ project boundaries execution එක සුරකියි.",
			),
			session(
				"APIs and Interactive Data Apps",
				["Call HTTP APIs safely and validate responses.", "Design a JSON endpoint with clear failure states.", "Build an interactive interface around a data workflow."],
				["HTTP", "JSON", "API contracts", "application state"],
				"Fetch a public dataset and expose a filtered analytical view.",
				"A documented API client and a small interactive app.",
				"An API is a contract between systems. We validate status, schema, and timeouts before data reaches analysis, then keep interface state separate from the data layer.",
				"API එකක් systems අතර contract එකකි. Data analysis එකට පෙර status, schema සහ timeout පරීක්ෂා කරමු. Interface state එක data layer එකෙන් වෙන් කර තබමු.",
			),
		],
		[
			("What makes an environment reproducible?", ["Declared versioned dependencies", "A long notebook", "A large dataset", "One branch"], 0),
			("Which HTTP status family indicates client errors?", ["4xx", "1xx", "2xx", "3xx"], 0),
			("What should an API client validate first?", ["Status and schema", "Chart colors", "Notebook title", "Commit count"], 0),
		],
		("Public Data Explorer", "Build a reproducible app that retrieves, validates, caches, filters, and visualizes a public API dataset.", "Reliability 30%, architecture 25%, interface 20%, documentation 15%, Git practice 10%."),
	),
	week(
		"Data Cleaning & Exploratory Analysis",
		"Create a defensible path from messy observations to analytical evidence.",
		[
			session(
				"Data Cleaning with Pandas",
				["Profile missingness, duplicates, types, and invalid ranges.", "Apply explicit rules without hiding data loss.", "Validate assumptions before and after transformation."],
				["data quality", "missing values", "types", "validation"],
				"Clean a noisy customers and orders dataset with an auditable rule log.",
				"A cleaning pipeline, validation report, and rejected-record table.",
				"Cleaning is a documented set of decisions about what fields mean and which observations remain trustworthy. We measure quality before and after every material rule.",
				"Data cleaning කියන්නේ fields වල අර්ථය සහ විශ්වාස කළ හැකි observations පිළිබඳ සටහන් කළ තීරණ මාලාවකි. වැදගත් rule එකකට පෙර සහ පසුව data quality මනිමු.",
			),
			session(
				"Exploratory Data Analysis",
				["Separate descriptive patterns from causal claims.", "Choose comparisons that fit the question.", "Document anomalies and competing explanations."],
				["distributions", "group comparisons", "correlation", "bias"],
				"Investigate retention differences and produce an evidence notebook.",
				"Five findings, each paired with evidence and a limitation.",
				"Exploration should reduce uncertainty, not decorate a notebook. We begin with a question, select a comparison, and state what the evidence cannot establish.",
				"Exploratory analysis එකේ අරමුණ uncertainty අඩු කිරීමයි. ප්‍රශ්නයකින් ආරම්භ කර සුදුසු comparison එකක් තෝරමු. Evidence එකෙන් කියන්න බැරි දේත් පැහැදිලිව සඳහන් කරමු.",
			),
		],
		[
			("What should accompany a cleaning rule?", ["A measurable rationale", "A random seed only", "A chart title", "A color"], 0),
			("What does correlation establish?", ["Association, not causation", "Causation", "Deployment readiness", "Ownership"], 0),
			("A strong finding includes evidence and what else?", ["A limitation", "A logo", "A password", "An endpoint"], 0),
		],
		("Evidence-First EDA", "Clean and investigate a customer dataset. Submit an auditable pipeline and five decision-relevant findings with limitations.", "Cleaning 30%, reasoning 30%, visual evidence 20%, limitations 10%, reproducibility 10%."),
	),
	week(
		"Feature Engineering & Pipelines",
		"Encode domain knowledge without leaking information across model boundaries.",
		[
			session(
				"Feature Engineering by Data Type",
				["Transform numeric, categorical, temporal, and text fields.", "Recognize target leakage.", "Compare engineered features against a baseline."],
				["encoding", "scaling", "time features", "leakage"],
				"Engineer behavioral features for a churn prediction problem.",
				"A feature dictionary with rationale and leakage review.",
				"A feature is a claim about information available when prediction occurs. We check timestamps and process boundaries so the model cannot learn from the future.",
				"Feature එකක් prediction එක කරන අවස්ථාවේ ලබාගත හැකි තොරතුරු පිළිබඳ claim එකකි. Timestamps සහ process boundaries පරීක්ෂා කර model එකට අනාගත data නොලැබෙන බව තහවුරු කරමු.",
			),
			session(
				"Reliable scikit-learn Pipelines",
				["Fit preprocessing only on training data.", "Compose column transforms and estimators.", "Persist and reload a complete inference artifact."],
				["fit and transform", "ColumnTransformer", "Pipeline", "serialization"],
				"Build a mixed-type preprocessing and model pipeline.",
				"A fitted pipeline, inference test, and feature contract.",
				"A pipeline makes training and inference execute the same transformations. Fitting stays inside training data, and the serialized artifact is tested with a realistic request.",
				"Pipeline එකක් training සහ inference දෙකේම එකම transformations ක්‍රියාත්මක කරයි. Fitting training data තුළ තබා save කළ artifact එක realistic request එකකින් පරීක්ෂා කරමු.",
			),
		],
		[
			("When should a scaler be fitted?", ["On training data only", "On all data", "After deployment", "On labels"], 0),
			("What is target leakage?", ["Using unavailable outcome information", "Dropping a column", "Renaming a feature", "Saving a model"], 0),
			("What does a pipeline protect?", ["Consistent ordered transformations", "Unlimited accuracy", "Free hosting", "Automatic labels"], 0),
		],
		("Leakage-Safe Feature Pipeline", "Design, fit, serialize, and test a mixed-type pipeline with a feature contract and leakage checklist.", "Boundary correctness 35%, rationale 25%, reproducibility 20%, tests 10%, explanation 10%."),
	),
	week(
		"Regression & Baseline Models",
		"Estimate continuous outcomes with interpretable baselines and robust evaluation.",
		[
			session(
				"Linear Regression and Baselines",
				["Establish naive and linear baselines.", "Interpret coefficients within assumptions.", "Diagnose residual patterns."],
				["baseline", "least squares", "coefficients", "residuals"],
				"Estimate delivery time and compare against a median baseline.",
				"A baseline report with residual diagnostics.",
				"A useful model must beat a credible simple rule. We start with the median, fit a linear model, and inspect residuals for structure the model missed.",
				"හොඳ model එකක් විශ්වාස කළ හැකි සරල baseline එකකට වඩා හොඳ විය යුතුය. Median එකෙන් ආරම්භ කර linear model එක fit කර model එකට අහිමි වූ patterns residuals මඟින් සොයමු.",
			),
			session(
				"Regularized and Nonlinear Regression",
				["Explain the bias-variance tradeoff.", "Use regularization to stabilize coefficients.", "Compare tree regressors with linear models."],
				["regularization", "bias and variance", "trees", "cross-validation"],
				"Compare ridge, lasso, and gradient boosting on house prices.",
				"A model comparison table and justified selection.",
				"Flexible models capture nonlinear structure but can fit noise. We choose complexity with validation evidence and inspect where each model earns its improvement.",
				"Flexible model එකකට nonlinear patterns හඳුනාගත හැකි නමුත් noise එකත් fit කළ හැක. Complexity තෝරන්නේ validation evidence මතය. සෑම model එකක්ම වැඩිදියුණු වන segments පරීක්ෂා කරමු.",
			),
		],
		[
			("Why start with a naive baseline?", ["To measure added value", "To maximize parameters", "To remove validation", "To guarantee fairness"], 0),
			("What can structured residuals indicate?", ["Missed model structure", "Perfect fit", "A secure API", "Causation"], 0),
			("What does regularization discourage?", ["Excessively large coefficients", "Test data", "Categories", "Version control"], 0),
		],
		("Regression Model Card", "Compare a naive baseline, regularized linear model, and tree regressor with residual and segment diagnostics.", "Evaluation 30%, diagnostics 25%, model choice 20%, reproducibility 15%, communication 10%."),
	),
	week(
		"Model Selection & Evaluation",
		"Make model decisions with valid boundaries and decision-aware metrics.",
		[
			session(
				"Validation, Cross-Validation and Tuning",
				["Choose splits that reflect future use.", "Tune without contaminating the test set.", "Search hyperparameters within a reproducible budget."],
				["holdout", "cross-validation", "time splits", "hyperparameters"],
				"Design validation schemes for random and temporal datasets.",
				"A validation protocol and reproducible tuning run.",
				"Validation simulates future use. We define the deployment boundary first, tune only inside training data, and keep one final test untouched.",
				"Validation කියන්නේ අනාගත භාවිතය simulate කිරීමකි. Deployment boundary එක මුලින් තීරණය කර training data තුළ පමණක් tuning කර අවසාන test set එක ස්පර්ශ නොකර තබමු.",
			),
			session(
				"Metrics, Error Analysis and Responsible Evaluation",
				["Map metrics to operational costs.", "Analyze meaningful data segments.", "Report uncertainty and failure modes."],
				["metric choice", "confidence", "segments", "failure modes"],
				"Write an evaluation memo for a high-impact prediction workflow.",
				"A decision memo with metrics, slices, and a release recommendation.",
				"A metric matters when its errors connect to real consequences. We translate error types into costs, inspect important groups, and include uncertainty in the release decision.",
				"Metric එකක වටිනාකම errors වල සැබෑ ප්‍රතිවිපාක සමඟ ඇති සම්බන්ධතාවයෙනි. Error types operational cost ලෙස බලමු. වැදගත් groups වෙන්ව පරීක්ෂා කර uncertainty සමඟ release recommendation එකක් දෙමු.",
			),
		],
		[
			("What should validation imitate?", ["Future deployment conditions", "A pretty chart", "Training loss only", "A filename"], 0),
			("When is the final test used?", ["After decisions are fixed", "During each tuning trial", "Before cleaning", "To create labels"], 0),
			("Why evaluate segments?", ["Aggregates can hide failures", "To reduce data", "To avoid docs", "To rename features"], 0),
		],
		("Evaluation Decision Memo", "Design a valid split, tune within a budget, and connect metrics and segment errors to business costs.", "Validity 35%, metric reasoning 25%, error analysis 20%, uncertainty 10%, communication 10%."),
	),
	week(
		"Classification Systems",
		"Build calibrated classification workflows and decision thresholds.",
		[
			session(
				"Logistic Regression, Probability and Thresholds",
				["Separate probability estimates from class decisions.", "Select a threshold from costs and capacity.", "Assess calibration and ranking."],
				["logistic regression", "probability", "thresholds", "calibration"],
				"Build a lead-prioritization model under a review-capacity limit.",
				"A threshold policy with calibration and cost analysis.",
				"A classifier produces a score before a class. The threshold belongs to the decision policy, so we choose it with costs, capacity, and calibrated probabilities.",
				"Classifier එකක් class එකකට පෙර score එකක් ලබා දෙයි. Threshold එක decision policy එකට අයත් නිසා costs, capacity සහ calibrated probabilities අනුව එය තෝරමු.",
			),
			session(
				"Trees, Ensembles and Imbalanced Data",
				["Compare ensembles with a linear baseline.", "Evaluate rare events with suitable metrics.", "Keep weighting or resampling inside training folds."],
				["decision trees", "ensembles", "class imbalance", "precision and recall"],
				"Detect rare payment failures and inspect false alarms.",
				"An imbalanced-classification report and operating point.",
				"Accuracy can look excellent when the event is rare. We examine precision and recall, keep resampling inside training folds, and match the operating point to action capacity.",
				"අවශ්‍ය event එක දුර්ලභ නම් accuracy ඉතා හොඳ ලෙස පෙනිය හැක. Precision සහ recall පරීක්ෂා කර resampling training folds තුළ තබමු. Operating point එක team capacity එකට ගැලපෙන්න තෝරමු.",
			),
		],
		[
			("What turns probability into an action class?", ["A threshold", "A file extension", "A scaler", "A commit"], 0),
			("Why can accuracy mislead on rare events?", ["The majority dominates it", "It has colors", "It needs SQL", "It equals recall"], 0),
			("Where should resampling occur?", ["Within training folds", "Before splitting", "On final test only", "After deployment"], 0),
		],
		("Rare-Event Classifier", "Compare linear and ensemble classifiers, assess calibration, and recommend a threshold under an explicit capacity.", "Leakage 25%, metrics 25%, threshold 20%, calibration 15%, communication 15%."),
	),
	week(
		"From Model to Deployed Service",
		"Package an end-to-end classifier as a tested, observable service.",
		[
			session(
				"End-to-End Classification Workflow",
				["Connect validation, preprocessing, training, and evaluation.", "Capture metadata and a repeatable training command.", "Define an inference schema."],
				["training workflow", "artifacts", "schemas", "model cards"],
				"Turn the week-seven experiment into a repeatable training pipeline.",
				"A versioned model artifact, schema, and model card.",
				"A production candidate includes preprocessing, configuration, schema, metrics, and limitations. We package those parts as one traceable release.",
				"Production candidate එකකට preprocessing, configuration, schema, metrics සහ limitations ඇතුළත්ය. එම සියලු කොටස් trace කළ හැකි එකම release එකක් ලෙස package කරමු.",
			),
			session(
				"Serving, Testing and Monitoring",
				["Expose inference through a validated endpoint.", "Test normal, boundary, and invalid requests.", "Define service, data, and model signals."],
				["REST inference", "contract tests", "logging", "drift"],
				"Serve the model with FastAPI and instrument structured logs.",
				"A container-ready API with tests and a monitoring specification.",
				"Serving adds a software contract around the model. We validate requests, return useful errors, test boundaries, and monitor service health, input shifts, and delayed outcomes.",
				"Serving මඟින් model එක වටා software contract එකක් එකතු වේ. Requests validate කර පැහැදිලි errors ලබා දී boundaries test කරමු. Service health, input shifts සහ delayed outcomes monitor කරමු.",
			),
		],
		[
			("What travels with a model artifact?", ["Preprocessing and schema", "Only a screenshot", "Only accuracy", "A password"], 0),
			("What should an inference API validate?", ["Request structure and values", "URL color", "GitHub stars", "Slide count"], 0),
			("What is data drift?", ["A change in input distribution", "A slow keyboard", "A deleted comment", "A branch"], 0),
		],
		("Production Inference Service", "Package a trained pipeline behind a validated API with contract tests, logs, health checks, and monitoring.", "API 25%, tests 25%, artifact 20%, observability 20%, documentation 10%."),
	),
	week(
		"Generative AI Applications",
		"Build grounded LLM experiences with measurable quality and safeguards.",
		[
			session(
				"LLM Foundations and Prompt Design",
				["Explain tokens, context, sampling, and limitations.", "Design structured prompts with testable outputs.", "Evaluate representative cases."],
				["tokens", "context windows", "prompt contracts", "evaluation"],
				"Create a structured data-quality assistant with an evaluation set.",
				"A prompt specification, test cases, and failure analysis.",
				"An LLM generates likely continuations; it does not query truth by default. We make instructions, context, and schemas explicit, then evaluate normal and adversarial cases.",
				"LLM එකක් likely continuation එකක් ජනනය කරන අතර ස්වයංක්‍රීයව සත්‍යය සොයන්නේ නැත. Instructions, context සහ schema පැහැදිලි කර normal හා adversarial cases මත evaluate කරමු.",
			),
			session(
				"Embeddings, RAG and Guardrails",
				["Build retrieval over a controlled document set.", "Trace answers to evidence.", "Apply access, safety, and fallback controls."],
				["embeddings", "retrieval", "grounding", "guardrails"],
				"Build a cited assistant over course policies and notes.",
				"A RAG prototype with retrieval evaluation and threat model.",
				"RAG supplies evidence at request time. We measure retrieval before final answers, require citations, and abstain when evidence or access is insufficient.",
				"RAG මඟින් request එකේදී evidence ලබා දෙයි. Final answer එකට පෙර retrieval quality මනිමු. Citations අවශ්‍ය කර evidence හෝ access ප්‍රමාණවත් නොවන විට පිළිතුරු නොදෙමු.",
			),
		],
		[
			("What does an LLM directly generate?", ["Likely token continuations", "Database truth", "Legal compliance", "Uptime"], 0),
			("What should be evaluated before a RAG answer?", ["Retrieval quality", "Logo size", "Commit color", "Price"], 0),
			("When should an assistant abstain?", ["When evidence is insufficient", "When output is short", "When a chart is blue", "After every citation"], 0),
		],
		("Grounded Knowledge Assistant", "Build and evaluate a cited RAG assistant with abstention, access controls, and prompt-injection safeguards.", "Retrieval 25%, grounding 25%, evaluation 20%, safeguards 20%, documentation 10%."),
	),
	week(
		"SQL, Data Modelling & Spark",
		"Transform analytical data from relational storage to distributed pipelines.",
		[
			session(
				"SQL and Analytical Data Modelling",
				["Write joins, aggregations, windows, and CTEs.", "Choose grain and keys before metrics.", "Test queries for duplication and missingness."],
				["joins", "window functions", "grain", "dimensional modelling"],
				"Model orders and customers, then compute retention and revenue.",
				"A documented SQL model with data tests.",
				"Reliable SQL begins with grain: what one row represents. We define keys before joining and test whether joins duplicate or discard business events.",
				"Reliable SQL එකක් grain එකෙන් ආරම්භ වේ, එනම් එක් row එකක අර්ථයයි. Join කිරීමට පෙර keys තීරණය කර events duplicate හෝ අහිමි වන්නේදැයි tests මඟින් තහවුරු කරමු.",
			),
			session(
				"Spark and Distributed ETL",
				["Explain partitions, shuffles, and lazy execution.", "Translate a local transform to Spark.", "Diagnose skew and avoid unnecessary movement."],
				["partitions", "lazy evaluation", "shuffles", "distributed joins"],
				"Scale an event aggregation from Pandas to PySpark.",
				"A Spark job with execution-plan notes and data checks.",
				"Distributed processing helps beyond one machine, but communication becomes expensive. We inspect partitions and plans, reduce shuffles, and preserve the data contract.",
				"Data එක machine එකකට වැඩි වූ විට distributed processing අවශ්‍ය නමුත් communication මිල අධික වේ. Partitions සහ plans පරීක්ෂා කර shuffles අඩු කර data contract එක සුරකිමු.",
			),
		],
		[
			("What does table grain define?", ["What one row represents", "A password", "A font", "A threshold"], 0),
			("What commonly duplicates metrics after joins?", ["Mismatched key cardinality", "A CTE name", "A comment", "A date"], 0),
			("What is often expensive in Spark?", ["Data shuffling", "A function name", "A variable", "A README"], 0),
		],
		("Analytical Pipeline at Two Scales", "Create validated SQL metrics and implement one large transformation in Spark with partition and shuffle analysis.", "Data model 25%, SQL 25%, Spark 25%, tests 15%, documentation 10%."),
	),
	week(
		"Cloud Delivery & MLOps",
		"Automate reliable releases and make model behavior observable.",
		[
			session(
				"Containers, Cloud Architecture and CI",
				["Package a minimal repeatable container.", "Separate runtime configuration from source.", "Build CI for tests, quality, and images."],
				["Docker", "configuration", "CI and CD", "cloud services"],
				"Containerize the inference service and run its CI workflow.",
				"A tested image, architecture diagram, and deployment runbook.",
				"A container standardizes the runtime, not the whole production system. Secrets stay outside the image, checks run before build, and infrastructure boundaries stay explicit.",
				"Container එක runtime එක standardize කරන නමුත් සම්පූර්ණ production system එක නොවේ. Secrets image එකෙන් පිටත තබා build කිරීමට පෙර tests ධාවනය කර infrastructure boundaries පැහැදිලි කරමු.",
			),
			session(
				"Experiments, Versioning and Monitoring",
				["Track code, data, parameters, metrics, and artifacts.", "Define promotion and rollback criteria.", "Design monitoring around model risks."],
				["experiment tracking", "model registry", "promotion", "observability"],
				"Create an experiment lineage and staged release checklist.",
				"A model release record, rollback plan, and alert specification.",
				"MLOps is disciplined change management for data and models. Every artifact links to evidence, promotion has an owner, and rollback does not require rebuilding the past.",
				"MLOps කියන්නේ data සහ models සඳහා disciplined change management එකකි. සෑම artifact එකක්ම evidence සමඟ සම්බන්ධ කර promotion owner සහ rollback process එක කලින්ම තීරණය කරමු.",
			),
		],
		[
			("Where should production secrets live?", ["Outside the image", "In source code", "In a slide", "In features"], 0),
			("What makes an experiment traceable?", ["Linked code, data, parameters, metrics, and artifacts", "A score only", "A screenshot", "A large image"], 0),
			("What should exist before promotion?", ["Rollback criteria and artifact", "A deleted test", "A new color", "A larger model"], 0),
		],
		("Releasable ML System", "Create a containerized CI-tested release with experiment lineage, architecture, promotion checks, alerts, and rollback.", "Reproducibility 25%, CI 20%, architecture 20%, lineage 20%, operations 15%."),
	),
	week(
		"Data Storytelling & Capstone",
		"Turn technical evidence into a defensible product decision and live demonstration.",
		[
			session(
				"Decision-Centred Data Storytelling",
				["Structure narrative around audience, decision, and evidence.", "Choose honest comparison charts.", "Communicate uncertainty clearly."],
				["audience", "narrative", "visual hierarchy", "uncertainty"],
				"Rewrite a technical analysis as a five-minute stakeholder briefing.",
				"A concise decision deck and evidence appendix.",
				"A data story is an argument for a decision supported by inspectable evidence. We identify audience and action first, remove irrelevant charts, and state uncertainty.",
				"Data story එකක් පරීක්ෂා කළ හැකි evidence මත decision එකක් සඳහා කරන argument එකකි. මුලින් audience සහ action තීරණය කර අවශ්‍ය නොවන charts ඉවත් කර uncertainty සඳහන් කරමු.",
			),
			session(
				"Capstone Integration and Demo",
				["Integrate data, modelling, software, and communication.", "Run a live demo with a tested fallback.", "Defend tradeoffs and define the next step."],
				["integration", "demo design", "tradeoffs", "roadmaps"],
				"Rehearse the capstone from problem statement to monitored prediction.",
				"A deployed capstone, repository, model card, deck, and demo recording.",
				"The capstone demonstrates valuable problem selection, trustworthy data, valid evaluation, reliable software, and an honest recommendation. We rehearse the path and prepare a fallback.",
				"Capstone එක valuable problem එකක සිට trustworthy data, valid evaluation, reliable software සහ honest recommendation දක්වා සම්පූර්ණ chain එක පෙන්වයි. Demo path එක rehearse කර fallback එකක් සූදානම් කරමු.",
			),
		],
		[
			("What should anchor a data story?", ["A decision for an audience", "Every chart", "The largest model", "Long methods"], 0),
			("Why prepare a demo fallback?", ["To preserve evidence if infrastructure fails", "To avoid testing", "To hide limits", "To replace code"], 0),
			("What should conclude a capstone?", ["The next operational test", "A claim of certainty", "Only training score", "An unrelated feature"], 0),
		],
		("Production-Minded Capstone", "Deliver a reproducible, validated, deployed data product with monitoring, model card, decision deck, and demo.", "Problem 20%, evaluation 20%, engineering 20%, usability 15%, communication 15%, responsibility 10%."),
	),
]
