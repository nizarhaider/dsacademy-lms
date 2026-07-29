# Week 10: Reliable Machine-Learning Pipelines

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who can train and evaluate a supervised model  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 10 presentation and related media.

---

## Slide 1 - Preprocessing Is Part of the Model

### Teaching purpose

Define a reliable training-to-inference contract.

### Learner-facing content

Raw tables often need **preprocessing** before a model can use them:

- impute missing values;
- scale numerical features;
- encode categories;
- select and order columns.

These steps learn parameters from training data, so they are part of the fitted model. Production inference must apply the same fitted transformations in the same order.

A **pipeline** binds preprocessing and prediction into one object with a shared `fit()` and `predict()` contract.

### Worked example

Training learns:

- median age `34`;
- salary mean and standard deviation;
- category mapping for city.

New rows must use those stored training values. Recalculating them on each request changes the model.

### Code example

```python
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

Expected output:

```text
Preprocessing is fitted on X_train and reused before every prediction.
```

### Visual description

Raw columns flow through fitted preprocessing and model blocks as one bounded pipeline.

### Instructor notes

Ask which steps learn from data. Any learned step must stay inside the training boundary.

### Notebook connection

The model-development notebook builds and saves a complete preprocessing and model pipeline.

### Sources

- [Scikit-learn: Pipelines and Composite Estimators](https://scikit-learn.org/stable/modules/compose.html)
- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)

---

## Slide 2 - Imputation Learns a Replacement Rule

### Teaching purpose

Explain why imputation must be fitted only on training data.

### Learner-facing content

**Imputation** replaces declared missing values using a rule.

Common simple rules:

- numerical median;
- numerical mean;
- most frequent category;
- constant marker such as `"missing"`.

The replacement value is a learned parameter. Fit it on training data, then apply the same value to validation, test, and production rows.

Imputation does not recover the unknown truth; it creates a usable value under an explicit assumption.

### Worked example

Training ages `[20, 30, missing, 100]`

Observed sorted values `[20,30,100]`; median `30`.  
Imputed training ages `[20,30,30,100]`.

If test ages are `[missing, 40]`, use training median `30`, not the test median.

### Code example

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median")
imputer.fit(X_train[["age"]])
```

Expected output:

```text
The fitted imputer stores the training-column median.
```

### Visual description

Training data determines median `30`; the stored value then fills missing cells in train and test branches.

### Instructor notes

Explain why `dropna()` is also a policy with possible selection bias, not a neutral cleanup.

### Notebook connection

Learners should inspect missing markers and justify each imputation strategy.

### Sources

- [Scikit-learn: Imputation of Missing Values](https://scikit-learn.org/stable/modules/impute.html)
- [Scikit-learn: SimpleImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html)

---

## Slide 3 - Scaling Changes Units, Not Row Meaning

### Teaching purpose

Define standardization and explain when scale matters.

### Learner-facing content

**Standardization** transforms a numerical value:

`z = (x - μ) / σ`

- `x`: original value
- `μ`: training-column mean
- `σ`: training-column standard deviation
- `z`: standardized value

After fitting, the training column has mean near zero and standard deviation near one.

Scaling matters for distance-based models, gradient optimization, and coefficient penalties. It does not make bad data valid.

### Worked example

Training mean `μ = 50`, standard deviation `σ = 10`.

For `x = 70`:

`z = (70 - 50) / 10`  
`= 20 / 10`  
`= 2`

The value is two standard deviations above the training mean.

### Code example

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train[["income"]])
```

Expected output:

```text
The scaler stores training mean and variance for later transforms.
```

### Visual description

Two features with different raw ranges are transformed to centred comparable scales; row order stays fixed.

### Instructor notes

Explain that tree models often do not require scaling, but mixed pipelines still need deliberate column rules.

### Notebook connection

The notebook's numerical preprocessing branch fits scaling inside the pipeline.

### Sources

- [Scikit-learn: StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- [Scikit-learn: Preprocessing Data](https://scikit-learn.org/stable/modules/preprocessing.html)

---

## Slide 4 - Encoding Represents Categories Numerically

### Teaching purpose

Explain one-hot encoding and unknown categories.

### Learner-facing content

Models usually require numerical inputs. **One-hot encoding** creates one binary column for each known category.

City values `Colombo`, `Kandy`, and `Galle` become columns such as:

`city_Colombo`, `city_Kandy`, `city_Galle`

One-hot encoding does not impose a false numerical order. The encoder must define what happens when production data contains an unseen category.

### Worked example

`Kandy` becomes:

`[0, 1, 0]`

The three positions correspond to the fitted category order. If `Jaffna` was unseen, `handle_unknown="ignore"` produces zeros for known category columns.

### Code example

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown="ignore")
encoder.fit(X_train[["city"]])
```

Expected output:

```text
The encoder stores categories observed in the training city column.
```

### Visual description

One city column expands into three binary columns with one active position per known city.

### Instructor notes

Contrast with replacing cities by `1,2,3`, which invents order and distance.

### Notebook connection

The categorical branch encodes values using categories learned only from training rows.

### Sources

- [Scikit-learn: OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html)
- [Scikit-learn: Encoding Categorical Features](https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features)

---

## Slide 5 - ColumnTransformer Applies Rules by Column Type

### Teaching purpose

Show how numerical and categorical branches combine.

### Learner-facing content

A **ColumnTransformer** applies different transformer sequences to selected columns and concatenates their outputs.

Example:

- numerical columns -> median imputer -> standard scaler;
- categorical columns -> most-frequent imputer -> one-hot encoder.

The transformed feature matrix may contain more columns than the raw table because one category column expands into several indicator columns.

### Worked example

Raw columns:

`age`, `income`, `city`

If city has three fitted categories, transformed columns are approximately:

`scaled_age`, `scaled_income`, `city_A`, `city_B`, `city_C`

Three raw columns become five model inputs.

### Code example

```python
from sklearn.compose import ColumnTransformer

preprocess = ColumnTransformer([
    ("numbers", numeric_pipeline, ["age", "income"]),
    ("categories", category_pipeline, ["city"]),
])
```

Expected output:

```text
One transformer that routes declared columns through two branches.
```

### Visual description

A table splits into numerical and categorical lanes, then recombines into one feature matrix.

### Instructor notes

Ask learners to predict output column count and explain what happens to unspecified columns.

### Notebook connection

The notebook uses `ColumnTransformer` to keep feature-specific preprocessing explicit.

### Sources

- [Scikit-learn: ColumnTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html)
- [Scikit-learn: Heterogeneous Data Example](https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html)

---

## Slide 6 - Pipeline Gives One Fit and Predict Boundary

### Teaching purpose

Explain pipeline execution order in training and inference.

### Learner-facing content

A scikit-learn **Pipeline** chains transformers and a final estimator.

During `fit(X_train, y_train)`:

1. fit the first transformer;
2. transform training data;
3. fit and transform each next transformer;
4. fit the final estimator.

During `predict(X_new)`:

1. transform with already-fitted transformers;
2. call the already-fitted estimator;
3. return predictions.

### Worked example

Pipeline:

`preprocess -> LogisticRegression`

One call to `fit()` learns imputers, scaler, encoder, and classifier. One call to `predict()` reuses all learned pieces in order.

### Code example

```python
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(max_iter=1000)),
])
```

Expected output:

```text
A composite estimator exposing fit, predict, and predict_proba.
```

### Visual description

Training arrows include fit-and-transform at each stage; inference arrows show transform-only then predict.

### Instructor notes

Explain why all steps except the last must transform data. Use named steps for inspection and tuning.

### Notebook connection

The source notebook's saved artifact is a pipeline rather than an estimator detached from preprocessing.

### Sources

- [Scikit-learn: Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
- [Scikit-learn: Getting Started Pipelines](https://scikit-learn.org/stable/getting_started.html#pipelines-chaining-pre-processors-and-estimators)

---

## Slide 7 - Pipelines Prevent Preprocessing Leakage

### Teaching purpose

Show exactly how cross-validation boundaries protect learned transformations.

### Learner-facing content

Unsafe sequence:

1. fit scaler on the complete dataset;
2. transform all rows;
3. split or cross-validate.

Validation information influences the scaler.

Safe sequence:

1. split training and test data;
2. put scaler and estimator inside a pipeline;
3. for each validation fold, fit the complete pipeline only on that fold's training rows;
4. transform the held-out fold with those fitted values.

### Worked example

Training fold values `[0,10]` have mean `5`. Validation value `[100]` must not change that mean.

If all values are used, mean becomes `(0+10+100)/3 = 36.67`, leaking validation information.

### Code example

```python
scores = cross_val_score(
    model, X_train, y_train, cv=5, scoring="roc_auc"
)
```

Expected output:

```text
Five scores, each produced by fitting the entire pipeline on four folds.
```

### Visual description

An unsafe all-data scaler is crossed out. Five safe fold diagrams each contain their own fitted preprocessing.

### Instructor notes

Use this example to show that leakage can occur without the target column.

### Notebook connection

Learners should never preprocess the complete table before notebook cross-validation.

### Sources

- [Scikit-learn: Data Leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
- [Scikit-learn: Pipelines Safety](https://scikit-learn.org/stable/modules/compose.html#pipeline-chaining-estimators)

---

## Slide 8 - Cross-Validation Measures Variation Across Splits

### Teaching purpose

Explain k-fold cross-validation and what its results mean.

### Learner-facing content

In **k-fold cross-validation**:

1. split training data into `k` folds;
2. fit on `k-1` folds;
3. validate on the remaining fold;
4. repeat until every fold has served as validation;
5. report scores and their variation.

Cross-validation supports model selection using training data. The untouched test set remains for final evaluation.

Use stratified, grouped, or time-aware splitting when the data structure requires it.

### Worked example

Five validation scores:

`[0.72, 0.75, 0.68, 0.78, 0.71]`

Mean:

`3.64 / 5 = 0.728`

Range `0.68` to `0.78` shows split-to-split variation.

### Code example

```python
scores = cross_val_score(model, X_train, y_train, cv=5)
print(scores.mean(), scores.std())
```

Expected output:

```text
The mean validation score and its standard deviation across folds.
```

### Visual description

A five-row fold diagram rotates the validation block, followed by a score distribution.

### Instructor notes

Do not present mean plus/minus standard deviation as a guaranteed confidence interval.

### Notebook connection

Learners will compare candidate pipelines using the same split strategy and metric.

### Sources

- [Scikit-learn: Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Scikit-learn: Model Selection](https://scikit-learn.org/stable/model_selection.html)

---

## Slide 9 - Model Comparison Must Use the Same Evidence

### Teaching purpose

Teach fair comparison and hyperparameter selection.

### Learner-facing content

A **hyperparameter** is a setting chosen before fitting, such as Ridge `alpha` or tree depth.

For fair comparison:

- use the same training rows and folds;
- fit each candidate's preprocessing inside each fold;
- use the same metric;
- compare baseline and candidate score distributions;
- consider latency, interpretability, memory, and failure behaviour;
- select using validation evidence;
- evaluate the final choice once on test data.

### Worked example

Cross-validation ROC-AUC:

Baseline `0.50`  
Logistic pipeline `0.74 ± 0.03`  
Tree pipeline `0.75 ± 0.08`

The tree's slightly higher mean comes with greater variation. The correct choice requires more than the largest mean.

### Code example

```python
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(
    model, {"classifier__C": [0.1, 1, 10]},
    cv=5, scoring="roc_auc"
)
```

Expected output:

```text
Each C value is evaluated through the complete pipeline across five folds.
```

### Visual description

Candidate distributions, not single bars, are compared beside operational constraints.

### Instructor notes

Explain double-underscore parameter names as step name plus parameter name.

### Notebook connection

The notebook's estimator comparison should preserve identical preprocessing and folds.

### Sources

- [Scikit-learn: GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)
- [Scikit-learn: Model Selection](https://scikit-learn.org/stable/model_selection.html)

---

## Slide 10 - Reproducibility Requires More Than a Random Seed

### Teaching purpose

Define the minimum experiment record.

### Learner-facing content

**Reproducibility** means another run can reconstruct the procedure and obtain expected results within known sources of variation.

Record:

- code revision;
- immutable data identity or checksum;
- feature and target schema;
- split method and random seed;
- library and Python versions;
- pipeline parameters;
- metrics for every fold and final test;
- hardware when relevant;
- generated model and reports.

A seed controls some randomness. It does not preserve changing data, code, packages, or hardware behaviour.

### Worked example

Two runs both use seed `42`, but one uses a changed CSV. Their results differ because the seed does not identify the training data.

### Code example

```python
experiment = {
    "seed": 42,
    "data_sha256": "...",
    "code_revision": "...",
    "metric": "roc_auc",
}
```

Expected output:

```text
A structured record connecting results to code, data, settings, and metric.
```

### Visual description

An experiment record links code, data, environment, parameters, metrics, and artifacts.

### Instructor notes

Distinguish repeatability on one machine from broader reproducibility.

### Notebook connection

Learners should save metadata beside the fitted pipeline and evaluation report.

### Sources

- [Scikit-learn: Controlling Randomness](https://scikit-learn.org/stable/common_pitfalls.html#controlling-randomness)
- [MLflow: Tracking](https://mlflow.org/docs/latest/ml/tracking/)

---

## Slide 11 - Persist the Whole Artifact and Load It Carefully

### Teaching purpose

Explain model serialization, compatibility, and trust boundaries.

### Learner-facing content

**Serialization** stores a fitted object so it can be loaded later.

Persist:

- complete preprocessing and estimator pipeline;
- input schema;
- label meanings and threshold;
- dependency versions;
- training data reference;
- validation and test evidence;
- artifact checksum.

Pickle-based formats can execute code when loaded. Load only trusted artifacts. Scikit-learn does not support loading a model across arbitrary version changes.

### Worked example

Saving only `LogisticRegression` loses the fitted encoder and scaler. A production row may then have the wrong number, order, or scale of features.

Saving the complete pipeline preserves the transformation order.

### Code example

```python
import joblib

joblib.dump(model, "model-pipeline.joblib")
loaded = joblib.load("model-pipeline.joblib")
```

Expected output:

```text
The loaded trusted artifact exposes the same pipeline prediction interface.
```

### Visual description

A complete sealed artifact contains preprocessing, estimator, schema, versions, metrics, and checksum. An incomplete estimator-only artifact is crossed out.

### Instructor notes

Emphasize trusted source and version compatibility before demonstrating loading.

### Notebook connection

The notebook's save step should persist the full pipeline and its metadata.

### Sources

- [Scikit-learn: Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [Joblib Persistence](https://joblib.readthedocs.io/en/latest/persistence.html)

---

## Slide 12 - Guided Lab: Build a Leakage-Safe Pipeline

### Teaching purpose

Set the Week 10 production-readiness exercise.

### Learner-facing content

Build and document:

1. numerical and categorical column lists;
2. missing-value policies;
3. numerical scaling;
4. categorical encoding with unknown handling;
5. `ColumnTransformer`;
6. estimator inside `Pipeline`;
7. task-appropriate cross-validation;
8. baseline and two candidate models;
9. selected hyperparameters;
10. untouched test result;
11. serialized complete pipeline and metadata;
12. a prediction after reload.

### Worked example

If the raw table has `2` numerical columns and one city column with `3` known categories, predict approximately `5` transformed columns. Confirm with `get_feature_names_out()` after fitting.

### Code example

```python
model.fit(X_train, y_train)
joblib.dump(model, "pipeline.joblib")
reloaded = joblib.load("pipeline.joblib")
assert np.array_equal(model.predict(X_test), reloaded.predict(X_test))
```

Expected output:

```text
The assertion passes for a trusted artifact loaded in the same environment.
```

### Visual description

A lab checklist spans schema, preprocessing branches, pipeline, cross-validation, test, persistence, and reload verification.

### Instructor notes

Inspect fold boundaries and reject any preprocessing fitted before cross-validation.

### Notebook connection

Complete the pipeline and save sections of `03.model-development.ipynb`.

### Sources

- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)
- [Scikit-learn: Pipelines and Composite Estimators](https://scikit-learn.org/stable/modules/compose.html)
