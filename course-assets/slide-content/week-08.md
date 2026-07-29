# Week 8: Classification and Model Evaluation

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who understand regression, held-out evaluation, and probabilities  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 8 presentation and related media.

---

## Slide 1 - Classification Predicts Categories or Their Probabilities

### Teaching purpose

Recap classification before introducing logistic regression.

### Learner-facing content

**Classification** is supervised learning with a categorical target.

- **Binary:** two classes, such as default/no default
- **Multiclass:** more than two classes, such as red/amber/green
- **Class probability:** estimated probability assigned to a class
- **Predicted class:** category chosen by a decision rule

Evaluation must represent the mistakes that matter. In medical screening, missing a positive case may cost more than an extra follow-up; in spam filtering, blocking valid mail may be especially costly.

### Worked example

Model output for positive class: `0.72`.

At threshold `0.50`, predict positive.  
At threshold `0.80`, predict negative.

The probability did not change; the decision rule changed.

### Code example

```python
probability = 0.72
prediction = int(probability >= 0.50)
print(prediction)
```

Expected output:

```text
1
```

### Visual description

A probability scale separates model output from two threshold-based decisions.

### Instructor notes

Ask learners to name the positive class explicitly; metric meanings depend on that choice.

### Notebook connection

The evaluation notebook compares actual labels, predicted labels, and predicted probabilities.

### Sources

- [Scikit-learn: Classification Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)

---

## Slide 2 - Logistic Regression Converts a Score into a Probability

### Teaching purpose

Explain the logistic-regression mechanism and every equation component.

### Learner-facing content

Logistic regression first calculates a linear score:

`z = β0 + βᵀx`

Then the **sigmoid** converts that score into a probability:

`P(y=1|x) = σ(z) = 1 / (1 + e^(-z))`

- `x`: feature vector
- `β`: learned coefficient vector
- `β0`: intercept
- `z`: real-valued score
- `e`: mathematical constant approximately `2.718`
- `σ(z)`: value between `0` and `1`

### Worked example

If `z = 1.386`:

`P = 1 / (1 + e^-1.386)`  
`≈ 1 / (1 + 0.250)`  
`≈ 0.80`

### Code example

```python
import math

z = 1.386
probability = 1 / (1 + math.exp(-z))
print(round(probability, 2))
```

Expected output:

```text
0.8
```

### Visual description

A weighted-sum block produces `z`, which enters an S-shaped sigmoid curve and exits as probability `0.80`.

### Instructor notes

Clarify that logistic regression is a classification algorithm despite “regression” in its name.

### Notebook connection

Scikit-learn's `predict_proba()` exposes the probabilities produced by the fitted classifier.

### Sources

- [Scikit-learn: Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [Scikit-learn: LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)

---

## Slide 3 - Thresholds Turn Probabilities into Actions

### Teaching purpose

Show how decision thresholds trade different errors.

### Learner-facing content

A **threshold** converts a positive-class probability into a predicted class:

`predict positive if P(y=1|x) >= threshold`

Lowering the threshold usually predicts more positives:

- more true positives may be found;
- more false positives may also be created.

Raising the threshold usually predicts fewer positives. Choose thresholds using validation data and real error costs, then evaluate the locked choice on test data.

### Worked example

Probabilities `[0.90, 0.70, 0.40, 0.20]`

At `0.50`: predictions `[1,1,0,0]`  
At `0.30`: predictions `[1,1,1,0]`

Only the third decision changes.

### Code example

```python
import numpy as np

probabilities = np.array([0.90, 0.70, 0.40, 0.20])
print((probabilities >= 0.30).astype(int))
```

Expected output:

```text
[1 1 1 0]
```

### Visual description

Four probability markers sit on a scale. Moving the threshold from 0.50 to 0.30 changes one class assignment.

### Instructor notes

Do not describe 0.50 as universally correct. Ask what happens when false negatives are more costly.

### Notebook connection

The notebook's ROC and confusion-matrix sections evaluate decisions across thresholds.

### Sources

- [Scikit-learn: Tuning the Decision Threshold](https://scikit-learn.org/stable/modules/classification_threshold.html)
- [Scikit-learn: Precision-Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)

---

## Slide 4 - A Confusion Matrix Counts Four Outcomes

### Teaching purpose

Build the foundation for classification metrics.

### Learner-facing content

For binary classification:

- **True positive (TP):** actual positive, predicted positive
- **False positive (FP):** actual negative, predicted positive
- **False negative (FN):** actual positive, predicted negative
- **True negative (TN):** actual negative, predicted negative

“Positive” is the class being detected. True/false says whether the prediction is correct; positive/negative says which class was predicted.

### Worked example

Actual `[1,1,1,0,0,0]`  
Predicted `[1,0,1,1,0,0]`

TP `= 2`  
FN `= 1`  
FP `= 1`  
TN `= 2`

Total `= 6`.

### Code example

```python
from sklearn.metrics import confusion_matrix

y_true = [1, 1, 1, 0, 0, 0]
y_pred = [1, 0, 1, 1, 0, 0]
print(confusion_matrix(y_true, y_pred))
```

Expected output:

```text
[[2 1]
 [1 2]]
```

### Visual description

A 2-by-2 matrix labels actual rows and predicted columns, with TN/FP/FN/TP positions and counts.

### Instructor notes

State scikit-learn's default label order `[0,1]`. Have learners classify each observation before counting.

### Notebook connection

All thresholded classification metrics can be traced back to these four counts.

### Sources

- [Scikit-learn: confusion_matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)
- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)

---

## Slide 5 - Accuracy Measures Overall Correctness

### Teaching purpose

Explain accuracy and its failure under imbalance.

### Learner-facing content

`accuracy = (TP + TN) / (TP + TN + FP + FN)`

Accuracy answers: “What fraction of all predictions were correct?”

It treats all rows and both error types equally. It can look strong when one class dominates, even if the minority class is never detected.

Always compare with class balance and a simple baseline.

### Worked example

From TP `2`, TN `2`, FP `1`, FN `1`:

`accuracy = (2 + 2) / 6 = 4/6 = 0.667`

For 95 negatives and 5 positives, always predicting negative gives `95%` accuracy and `0` true positives.

### Code example

```python
from sklearn.metrics import accuracy_score

print(round(accuracy_score(y_true, y_pred), 3))
```

Expected output:

```text
0.667
```

### Visual description

Four correct cells are highlighted among six. A second imbalanced grid shows high accuracy with every positive missed.

### Instructor notes

Do not ban accuracy; teach when its assumptions are inappropriate.

### Notebook connection

Learners will calculate accuracy beside precision, recall, and the class distribution.

### Sources

- [Scikit-learn: accuracy_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
- [Scikit-learn: DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)

---

## Slide 6 - Precision and Recall Answer Different Questions

### Teaching purpose

Define both metrics from the confusion matrix.

### Learner-facing content

`precision = TP / (TP + FP)`

Precision asks: “Of predicted positives, how many were actually positive?”

`recall = TP / (TP + FN)`

Recall asks: “Of actual positives, how many did we find?”

High precision limits false alarms. High recall limits missed positives. Neither alone describes the complete system.

### Worked example

TP `= 8`, FP `= 2`, FN `= 4`

Precision:

`8 / (8 + 2) = 8/10 = 0.80`

Recall:

`8 / (8 + 4) = 8/12 = 0.667`

### Code example

```python
from sklearn.metrics import precision_score, recall_score

print(precision_score(y_true, y_pred))
print(recall_score(y_true, y_pred))
```

Expected output:

```text
0.6666666666666666
0.6666666666666666
```

### Visual description

Precision zooms into the predicted-positive column; recall zooms into the actual-positive row.

### Instructor notes

Use the phrases “predicted positives” and “actual positives” repeatedly until learners can reconstruct the formulas.

### Notebook connection

The classification report contains precision and recall for each class.

### Sources

- [Scikit-learn: precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)
- [Scikit-learn: recall_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)

---

## Slide 7 - F1 Balances Precision and Recall

### Teaching purpose

Explain the harmonic mean and when F1 is useful.

### Learner-facing content

The F1 score is the harmonic mean of precision and recall:

`F1 = 2 x (precision x recall) / (precision + recall)`

F1 is high only when both precision and recall are high. It ignores true negatives, so it should be chosen because positive-class detection matters, not simply because it is popular.

For multiclass data, macro, micro, and weighted averaging answer different questions.

### Worked example

Precision `0.80`, recall `0.667`

`F1 = 2(0.80 x 0.667) / (0.80 + 0.667)`  
`= 1.0672 / 1.467`  
`≈ 0.727`

### Code example

```python
from sklearn.metrics import f1_score

print(round(f1_score(y_true, y_pred), 3))
```

Expected output:

```text
0.667
```

### Visual description

Precision and recall feed into the F1 equation. A comparison shows that one low input keeps F1 low.

### Instructor notes

Explain why F1 is not an average of all four confusion-matrix cells.

### Notebook connection

Learners should state the averaging method used in multiclass reports.

### Sources

- [Scikit-learn: f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
- [Scikit-learn: Classification Report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)

---

## Slide 8 - ROC-AUC Evaluates Ranking Across Thresholds

### Teaching purpose

Explain ROC curves and AUC without presenting them as universal quality.

### Learner-facing content

A ROC curve plots:

- true positive rate, which equals recall;
- false positive rate `FP / (FP + TN)`;
- across many thresholds.

**ROC-AUC** is the area under that curve. It summarizes how often a randomly chosen positive receives a higher score than a randomly chosen negative.

`0.5` is random ranking; `1.0` is perfect ranking. ROC-AUC does not select an operating threshold and can look optimistic under severe class imbalance.

### Worked example

Positive scores `[0.9, 0.7]` and negative scores `[0.6, 0.2]`.

Every positive score exceeds every negative except none in this case, so all four positive-negative pairs are correctly ranked. AUC is `1.0`.

### Code example

```python
from sklearn.metrics import roc_auc_score

y_true = [1, 1, 0, 0]
y_score = [0.9, 0.7, 0.6, 0.2]
print(roc_auc_score(y_true, y_score))
```

Expected output:

```text
1.0
```

### Visual description

A ROC plot shows diagonal random ranking and a curve above it. A note separates ranking quality from threshold choice.

### Instructor notes

Use probabilities or decision scores, not hard class labels, for AUC.

### Notebook connection

The notebook calculates ROC-AUC from model scores and plots the curve.

### Sources

- [Scikit-learn: roc_auc_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html)
- [Scikit-learn: ROC Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics)

---

## Slide 9 - Multiclass Metrics Need an Averaging Rule

### Teaching purpose

Explain one-vs-rest class metrics and macro/micro/weighted averages.

### Learner-facing content

For multiclass classification, treat each class as positive in turn.

- **Macro average:** unweighted mean across classes; each class counts equally.
- **Weighted average:** class metrics weighted by class support; common classes count more.
- **Micro average:** combine all decisions before calculating the metric.
- **Support:** number of actual examples for a class.

Always report the averaging rule and inspect class-level results.

### Worked example

Class recalls:

`A = 0.90`, `B = 0.60`, `C = 0.30`

Macro recall:

`(0.90 + 0.60 + 0.30) / 3 = 0.60`

This gives rare class C equal importance.

### Code example

```python
from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred))
```

Expected output:

```text
Precision, recall, F1, and support for each class plus stated averages.
```

### Visual description

Three class-level metric bars flow into macro, weighted, and micro aggregation diagrams.

### Instructor notes

Ask which averaging rule aligns with the project's decision priorities.

### Notebook connection

Learners should not quote only the final accuracy row from a classification report.

### Sources

- [Scikit-learn: Multiclass and Multioutput Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html#multiclass-and-multilabel-classification)
- [Scikit-learn: classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)

---

## Slide 10 - Regression Metrics Describe Numerical Error

### Teaching purpose

Complete the evaluation toolkit by distinguishing MAE, RMSE, and R².

### Learner-facing content

**MAE:** mean absolute error

`MAE = (1/n) Σ|yi - ŷi|`

**RMSE:** square root of mean squared error; gives larger residuals more influence.

**R²:** compares squared residuals with variation around the target mean.

MAE and RMSE use target units. R² is unitless and can be negative. Always pair a summary metric with residual inspection.

### Worked example

Residuals `[2, -4, 1]`

MAE: `(2 + 4 + 1) / 3 = 2.33`  
RMSE: `sqrt((4 + 16 + 1)/3) = sqrt(7) = 2.65`

RMSE is larger because it emphasizes the error of `4`.

### Code example

```python
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

print(mean_absolute_error(actual, predicted))
print(root_mean_squared_error(actual, predicted))
```

Expected output:

```text
2.3333333333333335
2.6457513110645907
```

### Visual description

The same residuals follow absolute-value and square-rooted-squared paths, ending in MAE and RMSE.

### Instructor notes

Reinforce that regression metrics do not evaluate class labels and classification metrics do not measure numerical distance.

### Notebook connection

The notebook contains separate classification and regression evaluation sections.

### Sources

- [Scikit-learn: Regression Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)
- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)

---

## Slide 11 - One Evaluation Report Needs Context

### Teaching purpose

Combine baseline, threshold, metrics, group checks, and uncertainty.

### Learner-facing content

A useful model report states:

1. test population and time period;
2. class counts or target distribution;
3. baseline;
4. locked threshold;
5. confusion matrix;
6. selected metrics with reasons;
7. error examples and group-level results;
8. probability calibration when probabilities drive decisions;
9. limitations and uncertainty.

A single score without a dataset and decision context is incomplete.

### Worked example

Fraud screen:

- baseline: always non-fraud;
- threshold chosen on validation data;
- report recall because missed fraud matters;
- report precision because investigations cost time;
- inspect performance by transaction size and region.

### Code example

```python
report = {
    "threshold": 0.35,
    "precision": 0.62,
    "recall": 0.84,
}
print(report)
```

Expected output:

```text
{'threshold': 0.35, 'precision': 0.62, 'recall': 0.84}
```

### Visual description

A report layout connects operating context, confusion matrix, metrics, slices, and limitations.

### Instructor notes

Ask what decision changes if the threshold moves. Require a reason for every selected metric.

### Notebook connection

Learners should turn notebook metric outputs into a decision-oriented evaluation report.

### Sources

- [Scikit-learn: Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Scikit-learn: Calibration](https://scikit-learn.org/stable/modules/calibration.html)

---

## Slide 12 - Guided Lab: Calculate Metrics from Counts

### Teaching purpose

Set the Week 8 practical assessment.

### Learner-facing content

For one binary classifier:

1. identify the positive class;
2. generate probabilities and choose a validation threshold;
3. calculate TP, FP, FN, and TN by hand;
4. calculate accuracy, precision, recall, and F1;
5. compare hand results with scikit-learn;
6. calculate ROC-AUC from scores;
7. compare with a majority-class baseline;
8. explain which error is more costly;
9. report one group-level check.

Also calculate MAE, RMSE, and R² for a separate regression example.

### Worked example

For TP `8`, FP `2`, FN `4`, TN `6`:

Accuracy `= 14/20 = 0.70`  
Precision `= 8/10 = 0.80`  
Recall `= 8/12 = 0.667`  
F1 `≈ 0.727`

### Code example

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, predictions))
```

Expected output:

```text
Class-level precision, recall, F1, and support matching the hand counts.
```

### Visual description

A lab flow moves from probabilities to threshold, confusion matrix, hand calculations, library verification, and decision recommendation.

### Instructor notes

Require intermediate counts before accepting metric output. Make learners state why the chosen positive class and threshold matter.

### Notebook connection

Complete `04.model-evaluation-techniques.ipynb`, using the slides to explain every metric formula before calling the API.

### Sources

- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)
- [Scikit-learn: Metrics and Scoring](https://scikit-learn.org/stable/modules/model_evaluation.html)
