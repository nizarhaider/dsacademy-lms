# Week 6: Machine Learning Fundamentals

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who understand tables, features, functions, and loss  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 6 presentation and related media.

---

## Slide 1 - Machine Learning Learns a Mapping from Examples

### Teaching purpose

Define machine learning without starting from an algorithm or library.

### Learner-facing content

**Machine learning (ML)** uses examples to estimate a function or discover structure.

A supervised model learns a mapping:

`features -> model -> prediction`

- A **feature** is an input available when a prediction is needed.
- A **target** is the value the model is trained to predict.
- A **model** is a parameterized function.
- A **prediction** is the model's output for new feature values.

Traditional programming supplies explicit rules. ML supplies examples and a learning procedure that estimates the rule.

### Worked example

Question: predict a house price.

Features: floor area, bedrooms, neighbourhood  
Target: sale price  
One observation: one sold house  
Prediction: an estimated price for a house whose true sale price is not yet known

### Code example

```python
features = {"area": 1200, "bedrooms": 3}
target = 185000
print(features, target)
```

Expected output:

```text
{'area': 1200, 'bedrooms': 3} 185000
```

### Visual description

Past labelled examples flow into training; a new feature row flows through the learned model into a prediction.

### Instructor notes

Ask what information exists at prediction time. Do not introduce a specific model class yet.

### Notebook connection

The model-development notebook separates feature columns from the target before training.

### Sources

- [Scikit-learn: Supervised Learning](https://scikit-learn.org/stable/supervised_learning.html)
- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)

---

## Slide 2 - Supervised and Unsupervised Learning Use Different Evidence

### Teaching purpose

Distinguish the two broad learning settings.

### Learner-facing content

**Supervised learning** uses examples with known targets. The model compares predictions with targets and learns from the error.

**Unsupervised learning** uses data without supplied targets. It searches for structure such as groups, lower-dimensional representations, or unusual observations.

The distinction is about available training evidence, not whether a human watches the computer.

### Worked example

Customer table with `annual_spend` and known `will_cancel`:

- predicting `will_cancel` is supervised;
- grouping customers by similar behaviour without a group label is unsupervised.

### Code example

```python
has_target = True
learning_type = "supervised" if has_target else "unsupervised"
print(learning_type)
```

Expected output:

```text
supervised
```

### Visual description

Two branches begin with the same feature table. One includes a target column and prediction error; the other produces discovered structure.

### Instructor notes

Ask learners whether targets exist in historical data and whether they match the actual business question.

### Notebook connection

The selected notebook is supervised because historical rows include a target used for training.

### Sources

- [Scikit-learn: User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Scikit-learn: Clustering](https://scikit-learn.org/stable/modules/clustering.html)

---

## Slide 3 - Regression Predicts a Quantity

### Teaching purpose

Teach the first major supervised problem type before linear regression.

### Learner-facing content

**Regression** predicts a continuous numerical target: a quantity that can take values across an interval.

Examples:

- house price: `185000.00`
- delivery time: `42.5` minutes
- energy use: `13.7` kWh

The output is not a category. A regression model may predict values not observed exactly in the training data.

Typical regression errors measure numerical distance between actual and predicted values.

### Worked example

Actual delivery time: `50` minutes  
Prediction: `46` minutes  
Residual: `actual - predicted = 50 - 46 = 4` minutes

The model under-predicted by `4` minutes.

### Code example

```python
actual = 50
predicted = 46
residual = actual - predicted
print(residual)
```

Expected output:

```text
4
```

### Visual description

A number line shows actual and predicted positions separated by a four-minute residual.

### Instructor notes

Use “continuous” to describe the target's meaning, even when stored measurements are rounded.

### Notebook connection

Week 7 introduces a specific regression algorithm and its equation.

### Sources

- [Scikit-learn: Supervised Learning](https://scikit-learn.org/stable/supervised_learning.html)
- [Scikit-learn: Regression Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)

---

## Slide 4 - Classification Predicts a Category

### Teaching purpose

Teach classification before logistic regression and metrics.

### Learner-facing content

**Classification** predicts a category or a probability for each category.

- **Binary classification:** two classes, such as spam/not spam
- **Multiclass classification:** more than two classes, such as low/medium/high risk
- A **label** is a categorical target value.

A classifier often estimates `P(class | features)`, then applies a decision rule. The predicted class is not the same thing as its probability.

### Worked example

Model output:

`P(spam | email) = 0.82`

With threshold `0.50`, predict spam because `0.82 >= 0.50`.  
With threshold `0.90`, predict not spam because `0.82 < 0.90`.

### Code example

```python
probability = 0.82
threshold = 0.50
prediction = "spam" if probability >= threshold else "not spam"
print(prediction)
```

Expected output:

```text
spam
```

### Visual description

A probability scale from 0 to 1 marks `0.82` and shows decisions under two thresholds.

### Instructor notes

Explain that threshold choice depends on the cost of different errors; Week 8 develops this.

### Notebook connection

The model-development and evaluation notebooks use categorical targets and probability-based metrics.

### Sources

- [Scikit-learn: Classification](https://scikit-learn.org/stable/supervised_learning.html)
- [Scikit-learn: Threshold Tuning](https://scikit-learn.org/stable/modules/classification_threshold.html)

---

## Slide 5 - Clustering Finds Groups Without Labels

### Teaching purpose

Complete the regression-classification-clustering distinction.

### Learner-facing content

**Clustering** is an unsupervised task that groups observations using a defined similarity or distance.

The clusters are discovered from features; no correct cluster label is supplied during training.

Clusters are not automatically real customer “types.” Their meaning depends on:

- selected features;
- scaling;
- distance rule;
- number or structure of clusters;
- stability across samples;
- domain interpretation.

### Worked example

Customers have two features: visits per month and average purchase.

The algorithm may identify frequent-low-spend and rare-high-spend groups. These names are interpretations added after examining the cluster centers.

### Code example

```python
problems = {
    "house price": "regression",
    "spam": "classification",
    "customer groups": "clustering",
}
print(problems)
```

Expected output:

```text
{'house price': 'regression', 'spam': 'classification', 'customer groups': 'clustering'}
```

### Visual description

A scatter plot shows unlabelled points, then the same points coloured into groups after clustering.

### Instructor notes

Avoid teaching k-means mechanics here. Focus on the absence of target labels and the need for interpretation.

### Notebook connection

Clustering is included for problem framing; the core notebook lab remains supervised.

### Sources

- [Scikit-learn: Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [Scikit-learn: Preprocessing Data](https://scikit-learn.org/stable/modules/preprocessing.html)

---

## Slide 6 - Training Estimates Parameters; Inference Uses Them

### Teaching purpose

Separate learning-time behaviour from prediction-time behaviour.

### Learner-facing content

**Training** estimates model parameters using historical examples.

**Inference** applies fixed learned parameters to new feature values to produce predictions.

During training:

1. calculate predictions;
2. compare with known targets;
3. measure loss;
4. update parameters;
5. repeat.

During inference, the true target is not required and parameters should not change.

### Worked example

Training row: features `[area=1200, bedrooms=3]`, target `185000`.  
Inference row: features `[area=1350, bedrooms=3]`, target unknown.  
The model returns an estimated price using parameters learned earlier.

### Code example

```python
model.fit(X_train, y_train)
predictions = model.predict(X_new)
```

Expected output:

```text
One prediction for each row in X_new.
```

### Visual description

Training is a loop with targets and updates. Inference is a one-way path with no target and no update.

### Instructor notes

Explain `fit` and `predict` conceptually; model selection and pipelines appear later.

### Notebook connection

The notebook uses `fit()` on training data and `predict()` on held-out data.

### Sources

- [Scikit-learn: Getting Started](https://scikit-learn.org/stable/getting_started.html)
- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)

---

## Slide 7 - Train, Validation, and Test Sets Have Different Jobs

### Teaching purpose

Explain data splitting as protection against self-evaluation.

### Learner-facing content

- **Training set:** estimates model parameters.
- **Validation set:** compares model choices and settings.
- **Test set:** estimates final performance after choices are complete.

If test results influence repeated model changes, the test set becomes another validation set and no longer provides an independent final estimate.

Splits should represent future use. Time-ordered, grouped, or repeated-person data may require specialized splitting instead of random rows.

### Worked example

From `1,000` independent observations:

- training: `700`
- validation: `150`
- test: `150`

The exact percentages are less important than keeping roles separate and documenting the split.

### Code example

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

Expected output:

```text
80% of rows in the training split and 20% in the test split.
```

### Visual description

One dataset bar splits into labelled train, validation, and test sections with arrows showing permitted use.

### Instructor notes

State that the code example creates two sets; cross-validation in Week 10 can provide validation within training data.

### Notebook connection

Learners should identify which notebook rows train the model and which estimate generalization.

### Sources

- [Scikit-learn: Model Selection](https://scikit-learn.org/stable/model_selection.html)
- [Scikit-learn: train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)

---

## Slide 8 - Generalization Is Performance on Unseen Examples

### Teaching purpose

Define underfitting, overfitting, and the generalization gap.

### Learner-facing content

**Generalization** is useful performance on representative examples that did not influence fitting.

- **Underfitting:** the model is too limited or poorly trained to capture important structure.
- **Overfitting:** the model learns training-specific noise and performs worse on new data.
- **Generalization gap:** difference between training and validation performance.

More training accuracy does not guarantee a better model. The goal is reliable unseen-data performance.

### Worked example

Model A: training accuracy `70%`, validation `69%`  
Model B: training accuracy `99%`, validation `74%`

Model B fits training data much more closely, but its `25`-point gap signals overfitting risk.

### Code example

```python
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(train_score - test_score)
```

Expected output:

```text
The observed generalization gap for the chosen score.
```

### Visual description

Three fitted curves show underfit, appropriate fit, and overfit against the same data.

### Instructor notes

Avoid defining overfitting only as “high training score.” It requires comparison with unseen data.

### Notebook connection

The notebook's evaluation section checks held-out performance rather than training fit alone.

### Sources

- [Scikit-learn: Underfitting vs Overfitting](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html)
- [Scikit-learn: Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

---

## Slide 9 - A Baseline Sets the Minimum Standard

### Teaching purpose

Teach learners to compare models with simple credible rules.

### Learner-facing content

A **baseline** is a simple rule used as a reference.

Regression baseline: always predict the training-target mean.  
Classification baseline: always predict the most frequent training class.

A complex model must beat the baseline on relevant unseen-data metrics. Otherwise, it has not demonstrated useful learning.

The baseline must be fitted using training data only.

### Worked example

Training prices: `[100, 120, 140]`  
Mean baseline: `(100 + 120 + 140) / 3 = 120`

For test targets `[110, 150]`, predictions are `[120, 120]`.  
Absolute errors are `[10, 30]`; MAE is `(10 + 30) / 2 = 20`.

### Code example

```python
from sklearn.dummy import DummyRegressor

baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
```

Expected output:

```text
A fitted baseline that predicts the training-target mean.
```

### Visual description

A simple baseline bar and a model bar stand beside a minimum-performance line.

### Instructor notes

Explain why the test-target mean must not be used: it would reveal information unavailable at prediction time.

### Notebook connection

Learners should compare the notebook model with a task-appropriate dummy estimator.

### Sources

- [Scikit-learn: Dummy Estimators](https://scikit-learn.org/stable/modules/model_evaluation.html#dummy-estimators)
- [Scikit-learn: DummyRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html)

---

## Slide 10 - Leakage Gives the Model Unfair Information

### Teaching purpose

Define target and preprocessing leakage before model pipelines.

### Learner-facing content

**Data leakage** occurs when training uses information that would not be available at real prediction time or should belong only to validation/test data.

Examples:

- using final payment status to predict whether payment will occur;
- calculating scaling values from the complete dataset before splitting;
- imputing test values using statistics from test rows;
- including duplicate people in both training and test sets.

Leakage can produce excellent evaluation scores and poor real-world performance.

### Worked example

Goal: predict cancellation one month in advance.  
Feature: `cancellation_date`.

This feature directly reveals the future target and is unavailable one month earlier. It must not be used.

### Code example

```python
X = df.drop(columns=["will_cancel", "cancellation_date"])
y = df["will_cancel"]
```

Expected output:

```text
Features exclude the target and the future-revealing column.
```

### Visual description

A time line marks prediction time. Allowed features appear before it; a forbidden future feature appears after it.

### Instructor notes

For every feature, ask “When is this value created?” Week 10 will prevent preprocessing leakage with pipelines.

### Notebook connection

Learners must audit features before running the model-development pipeline.

### Sources

- [Scikit-learn: Data Leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)

---

## Slide 11 - Evaluation Must Match the Problem

### Teaching purpose

Connect problem type, outputs, and evidence without teaching all formulas yet.

### Learner-facing content

Evaluation asks whether model errors are acceptable for the intended decision.

Regression compares numerical prediction distance, using measures such as MAE, RMSE, and R².

Classification compares predicted and actual classes or probabilities, using measures such as precision, recall, F1, and ROC-AUC.

Metrics are not interchangeable. Accuracy does not evaluate house-price distance, and RMSE does not describe spam categories.

Also inspect errors across important groups, time periods, and operating thresholds.

### Worked example

- Delivery-time prediction -> regression -> errors in minutes
- Fraud detection -> classification -> missed fraud and false alarms have different costs
- Customer segmentation -> clustering -> no supplied correct label; evaluate stability and usefulness

### Code example

```python
task = "classification"
metric_family = "confusion-matrix metrics" if task == "classification" else "distance metrics"
print(metric_family)
```

Expected output:

```text
confusion-matrix metrics
```

### Visual description

Three task cards map regression, classification, and clustering to different output and evaluation evidence.

### Instructor notes

Keep formulas for Weeks 7 and 8. Focus on selecting evidence that matches the prediction target and decision.

### Notebook connection

The evaluation notebook deepens the metrics after learners can frame the problem correctly.

### Sources

- [Scikit-learn: Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)

---

## Slide 12 - Guided Lab: Frame the Problem Before Modelling

### Teaching purpose

Make problem framing the Week 6 deliverable.

### Learner-facing content

For five proposed ML projects, identify:

1. one observation;
2. features available at prediction time;
3. target, if one exists;
4. regression, classification, or clustering;
5. training and inference moments;
6. split strategy;
7. baseline;
8. evaluation evidence;
9. one leakage risk.

Then select one project and draw its complete data flow before running the Week 6 notebook.

### Worked example

Project: predict tomorrow's electricity demand.

Observation: one region-hour  
Target: next-hour kWh  
Task: regression  
Split: time-ordered  
Baseline: previous day's same-hour demand  
Leakage risk: using measurements recorded after the prediction time

### Code example

```python
problem = {
    "observation": "one region-hour",
    "target": "next-hour kWh",
    "task": "regression",
}
print(problem)
```

Expected output:

```text
{'observation': 'one region-hour', 'target': 'next-hour kWh', 'task': 'regression'}
```

### Visual description

A worksheet maps business question to observation, features, target, task, split, baseline, metric, and leakage check.

### Instructor notes

Do not allow algorithm names until the problem definition is complete. Challenge features that may be unavailable at prediction time.

### Notebook connection

Continue into `03.model-development.ipynb`, labelling each section as data preparation, training, inference, or evaluation.

### Sources

- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)
- [Scikit-learn: Getting Started](https://scikit-learn.org/stable/getting_started.html)
