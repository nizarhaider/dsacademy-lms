# Week 7: Linear Regression

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who can distinguish regression from classification  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 7 presentation and related media.

---

## Slide 1 - Linear Regression Predicts a Continuous Target

### Teaching purpose

Place linear regression inside the supervised regression category.

### Learner-facing content

**Linear regression** is a supervised algorithm for predicting a continuous numerical target with a weighted sum of features.

Examples include price, duration, demand, and energy use. It is not a classification algorithm: its direct output is a number on a continuous scale, not a class probability.

The word **linear** means the prediction is linear in the model's coefficients. Each coefficient contributes through multiplication and addition.

### Worked example

Question: predict delivery time in minutes from distance in kilometres.

Feature `x`: distance  
Target `y`: actual delivery time  
Prediction `ŷ`: estimated delivery time

If the model predicts `42` for an actual time of `45`, the residual is `45 - 42 = 3` minutes.

### Code example

```python
task = "predict delivery minutes"
problem_type = "regression"
print(task, problem_type)
```

Expected output:

```text
predict delivery minutes regression
```

### Visual description

A task map places linear regression under supervised learning, then regression, beside a continuous number line.

### Instructor notes

Ask learners why yes/no late delivery would be classification while delivery minutes is regression.

### Notebook connection

The model-development notebook fits estimators to numerical targets; this week explains the first model equation.

### Sources

- [Scikit-learn: Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)
- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)

---

## Slide 2 - The Linear Regression Equation Has Four Parts

### Teaching purpose

Introduce the complete equation and define every symbol.

### Learner-facing content

For `n` features:

`ŷ = β0 + β1x1 + β2x2 + ... + βnxn`

- `ŷ` (y-hat): predicted target
- `β0`: intercept, the prediction when all features equal zero
- `xi`: value of feature `i`
- `βi`: coefficient for feature `i`
- `n`: number of features

Each term `βixi` is one feature's contribution. The model adds all contributions and the intercept.

### Worked example

`ŷ = 10 + 4x`

For distance `x = 5`:

`ŷ = 10 + 4(5)`  
`= 10 + 20`  
`= 30` minutes

### Code example

```python
intercept = 10
coefficient = 4
distance = 5
prediction = intercept + coefficient * distance
print(prediction)
```

Expected output:

```text
30
```

### Visual description

The equation is colour-coded so `ŷ`, `β0`, `β1`, and `x1` connect to their definitions and example values.

### Instructor notes

Read the equation in words before substituting values. Explain that coefficients and intercept are learned from training data.

### Notebook connection

Scikit-learn stores learned values in `intercept_` and `coef_`.

### Sources

- [Scikit-learn: Ordinary Least Squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares)
- [Scikit-learn: LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)

---

## Slide 3 - A Coefficient Describes a Conditional Change

### Teaching purpose

Teach correct interpretation of slope and intercept.

### Learner-facing content

In a one-feature model, the coefficient is the predicted change in `ŷ` for a one-unit increase in `x`.

In a multiple-feature model, coefficient `βi` is the predicted change for one unit of feature `xi` **while other model features are held constant**.

The intercept may not have a practical interpretation if all features being zero is impossible or outside the observed data.

A coefficient describes the fitted association in the model. It does not prove causation.

### Worked example

`price = 50,000 + 120 x area`

If area is measured in square metres, the model associates one additional square metre with `120` more price units, holding other included features constant.

For area `100`: `50,000 + 120(100) = 62,000`.

### Code example

```python
def predict_price(area):
    return 50000 + 120 * area

print(predict_price(100))
```

Expected output:

```text
62000
```

### Visual description

A line shows intercept at `50,000` and a rise of `120` for one unit of area. A warning marks extrapolation beyond observed area.

### Instructor notes

Require units in every interpretation. Avoid saying that area “causes” price.

### Notebook connection

Learners should inspect coefficient signs, magnitudes, feature units, and preprocessing before interpretation.

### Sources

- [Scikit-learn: Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)
- [OpenStax: Linear Functions](https://openstax.org/books/college-algebra-2e/pages/2-1-linear-functions)

---

## Slide 4 - Multiple Features Add Separate Contributions

### Teaching purpose

Extend the equation to a realistic feature vector and dot product.

### Learner-facing content

With several features, linear regression can be written:

`ŷ = β0 + x · β`

`x · β` is the dot product:

`x1β1 + x2β2 + ... + xnβn`

Feature order must match coefficient order. Changing units changes coefficient size, which is why raw coefficient magnitudes are not automatically comparable.

### Worked example

Model:

`ŷ = 20 + 3(distance) - 2(items)`

For distance `5` and items `4`:

`ŷ = 20 + 3(5) - 2(4)`  
`= 20 + 15 - 8`  
`= 27` minutes

### Code example

```python
import numpy as np

x = np.array([5, 4])
beta = np.array([3, -2])
prediction = 20 + x @ beta
print(prediction)
```

Expected output:

```text
27
```

### Visual description

Two feature-coefficient pairs produce contributions `+15` and `-8`; these join intercept `20` to make `27`.

### Instructor notes

Ask learners to calculate each contribution separately and identify its unit.

### Notebook connection

The feature matrix has one column per coefficient and one row per prediction.

### Sources

- [Scikit-learn: LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Mathematics for Machine Learning](https://mml-book.github.io/)

---

## Slide 5 - Residuals Show Individual Prediction Errors

### Teaching purpose

Define residuals and their signs.

### Learner-facing content

A **residual** is actual minus predicted:

`ei = yi - ŷi`

- positive residual: the model predicted too low;
- negative residual: the model predicted too high;
- zero residual: prediction matched the observed target.

Residual plots help reveal patterns that a single score hides. A useful linear fit usually leaves residuals scattered around zero without a clear curve or funnel shape.

### Worked example

Actual `[30, 40, 50]`  
Predicted `[28, 44, 49]`

Residuals:

`30 - 28 = 2`  
`40 - 44 = -4`  
`50 - 49 = 1`

### Code example

```python
actual = np.array([30, 40, 50])
predicted = np.array([28, 44, 49])
print(actual - predicted)
```

Expected output:

```text
[ 2 -4  1]
```

### Visual description

Observed points and fitted points are connected by vertical residual lines; signs are labelled.

### Instructor notes

Keep the convention `actual - predicted` consistent. Some systems define error differently, so always state the formula.

### Notebook connection

The evaluation notebook later plots and summarizes residuals for regression.

### Sources

- [Scikit-learn: Prediction Error Plot](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_predict.html)
- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)

---

## Slide 6 - MSE and RMSE Summarize Residuals

### Teaching purpose

Calculate squared-error loss and restore target units.

### Learner-facing content

Mean squared error:

`MSE = (1/n) Σ(yi - ŷi)^2`

Root mean squared error:

`RMSE = sqrt(MSE)`

Squaring makes all terms non-negative and gives larger residuals more influence. MSE is in squared target units; RMSE returns to the original target units.

### Worked example

Residuals `[2, -4, 1]`

Squared: `[4, 16, 1]`  
Sum: `21`  
`MSE = 21 / 3 = 7`  
`RMSE = sqrt(7) ≈ 2.65`

### Code example

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(actual, predicted)
rmse = mse ** 0.5
print(mse, round(rmse, 2))
```

Expected output:

```text
7.0 2.65
```

### Visual description

A calculation table transforms residuals into squared residuals, mean, and square root with units shown at each stage.

### Instructor notes

Explain why RMSE is easier to communicate while MSE is convenient for optimization.

### Notebook connection

Learners will compare regression models using held-out RMSE and other metrics.

### Sources

- [Scikit-learn: mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
- [Scikit-learn: root_mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html)

---

## Slide 7 - Ordinary Least Squares Chooses the Best Coefficients

### Teaching purpose

Explain fitting as an optimization objective rather than a magic library call.

### Learner-facing content

**Ordinary least squares (OLS)** chooses coefficients that minimize the sum of squared residuals:

`minβ Σ(yi - ŷi)^2`

Each candidate line produces residuals. Squaring and summing gives one cost. OLS selects the coefficients with the smallest cost among the candidates considered by the solver.

With one feature, the result is the fitted line. With many features, it is a fitted plane or higher-dimensional hyperplane.

### Worked example

Candidate A squared residuals: `[1, 4, 1]`, sum `6`  
Candidate B squared residuals: `[4, 9, 1]`, sum `14`

OLS prefers Candidate A because `6 < 14`.

### Code example

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
print(model.intercept_, model.coef_)
```

Expected output:

```text
One learned intercept and one coefficient for each feature.
```

### Visual description

Two candidate lines appear over points; residual squares are totalled and the lower-cost line is selected.

### Instructor notes

Clarify that “best” means lowest squared error on training data, not automatically best generalization or causality.

### Notebook connection

The notebook's `fit()` call invokes a solver for this objective.

### Sources

- [Scikit-learn: Ordinary Least Squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares)
- [Scikit-learn: LinearRegression Notes](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)

---

## Slide 8 - Gradient Descent Can Minimize the Same Loss

### Teaching purpose

Connect Week 5 optimization to linear regression.

### Learner-facing content

Instead of solving least squares directly, an iterative method can:

1. start with coefficient values;
2. predict training targets;
3. calculate MSE;
4. calculate gradients;
5. update coefficients opposite the gradients;
6. repeat.

Update:

`β_new = β_old - η ∂MSE/∂β`

OLS describes the objective. A closed-form or numerical solver and gradient descent are different procedures for reducing that objective.

### Worked example

Current coefficient `β = 2`, gradient `-6`, learning rate `0.1`:

`β_new = 2 - 0.1(-6)`  
`= 2 + 0.6`  
`= 2.6`

The negative gradient means increasing the coefficient locally reduces loss.

### Code example

```python
beta = 2.0
gradient = -6.0
beta = beta - 0.1 * gradient
print(beta)
```

Expected output:

```text
2.6
```

### Visual description

A coefficient point takes one labelled step down an MSE curve; the update equation is expanded beside it.

### Instructor notes

Explain that gradients are recomputed after every step and convergence depends on scale and learning rate.

### Notebook connection

This mechanism reappears in PyTorch training, even when the model is nonlinear.

### Sources

- [Scikit-learn: SGDRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html)
- [Dive into Deep Learning: Linear Regression Implementation](https://d2l.ai/chapter_linear-regression/linear-regression-scratch.html)

---

## Slide 9 - Assumptions Tell Us When the Model Is Credible

### Teaching purpose

Introduce diagnostic assumptions in plain language.

### Learner-facing content

For interpretation and uncertainty estimates, common linear-regression assumptions include:

- the mean target relationship is reasonably linear in the included terms;
- residuals are independent under the sampling process;
- residual variance is roughly constant across fitted values;
- no observation has excessive influence;
- features do not contain perfect linear duplication.

Normal residuals matter mainly for some small-sample statistical inferences, not for calculating predictions.

### Worked example

If residual spread grows from about `±2` to `±20` as predictions increase, variance is not constant. One RMSE value hides that the model is much less reliable for large predictions.

### Code example

```python
residuals = y_test - model.predict(X_test)
plt.scatter(model.predict(X_test), residuals)
plt.axhline(0, color="black")
```

Expected output:

```text
A residual plot centred on a horizontal zero line.
```

### Visual description

Three residual plots show random scatter, curved pattern, and funnel-shaped variance.

### Instructor notes

Frame assumptions as questions to investigate, not boxes that make a model universally true.

### Notebook connection

Learners should inspect residuals and data collection before trusting coefficients.

### Sources

- [NIST: Residual Analysis](https://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm)
- [Statsmodels: Regression Diagnostics](https://www.statsmodels.org/stable/examples/notebooks/generated/regression_diagnostics.html)

---

## Slide 10 - Evaluate Against a Mean Baseline on Unseen Data

### Teaching purpose

Combine baseline, split, RMSE, and R².

### Learner-facing content

Fit coefficients on training data and evaluate once on held-out data.

A mean baseline predicts the training-target mean for every new row.

`R² = 1 - SSres / SStot`

- `SSres`: squared residual sum for the model
- `SStot`: squared deviation sum from the target mean

`R² = 1` is perfect on that dataset, `0` matches the mean baseline under the formula, and negative values are worse.

### Worked example

If `SSres = 20` and `SStot = 80`:

`R² = 1 - 20/80 = 1 - 0.25 = 0.75`

The model reduces squared error by 75% relative to the mean reference on these examples.

### Code example

```python
from sklearn.metrics import root_mean_squared_error, r2_score

pred = model.predict(X_test)
print(root_mean_squared_error(y_test, pred))
print(r2_score(y_test, pred))
```

Expected output:

```text
One RMSE in target units and one unitless R² value.
```

### Visual description

Baseline and fitted-model predictions are compared on the same test rows with RMSE and R² labels.

### Instructor notes

Do not describe R² as percentage accuracy. Explain it relative to squared variation around the mean.

### Notebook connection

The evaluation notebook calculates RMSE and R² for regression predictions.

### Sources

- [Scikit-learn: r2_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)
- [Scikit-learn: DummyRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html)

---

## Slide 11 - Ridge and Lasso Control Coefficient Size

### Teaching purpose

Introduce regularization as a modification to the fitting objective.

### Learner-facing content

**Regularization** adds a penalty for coefficient size.

Ridge:

`SSE + α Σβj²`

Lasso:

`SSE + α Σ|βj|`

- `SSE`: sum of squared residuals
- `α`: penalty strength
- Ridge usually shrinks coefficients toward zero.
- Lasso can set some coefficients exactly to zero.

Features should normally be scaled before comparing penalty effects. Choose `α` with validation evidence, not the test set.

### Worked example

Two models have equal SSE. Model A has coefficients `[10, 10]`; Model B has `[4, 5]`.

Ridge penalties:

A: `10² + 10² = 200`  
B: `4² + 5² = 41`

With `α > 0`, the objective prefers the smaller coefficient norm.

### Code example

```python
from sklearn.linear_model import Ridge, Lasso

ridge = Ridge(alpha=1.0)
lasso = Lasso(alpha=0.1)
```

Expected output:

```text
Two regression estimators with different coefficient penalties.
```

### Visual description

OLS, Ridge, and Lasso coefficient bars show no penalty, shrinkage, and sparse zero coefficients.

### Instructor notes

Do not claim regularization always improves performance. It trades training fit for lower variance and must be validated.

### Notebook connection

Week 10 places scaling and regularized models inside leakage-safe pipelines.

### Sources

- [Scikit-learn: Ridge Regression](https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification)
- [Scikit-learn: Lasso](https://scikit-learn.org/stable/modules/linear_model.html#lasso)

---

## Slide 12 - Guided Lab: Explain Every Part of a Regression

### Teaching purpose

Set the Week 7 notebook-readiness task.

### Learner-facing content

Build a small delivery-time regression and report:

1. observation, features, and continuous target;
2. baseline test RMSE;
3. fitted equation with units;
4. one prediction calculated by hand;
5. residuals, MSE, RMSE, and R²;
6. a residual plot;
7. one assumption concern;
8. one comparison with Ridge.

The deliverable must explain what each coefficient means and what it does not prove.

### Worked example

For `ŷ = 20 + 3(distance) - 2(items)` and `[5,4]`:

Prediction `27`; actual `30`; residual `3`; squared residual `9`.

### Code example

```python
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(model.intercept_, model.coef_)
```

Expected output:

```text
One intercept, one coefficient per feature, and test predictions.
```

### Visual description

A lab checklist follows problem type, equation, hand prediction, fit, residuals, metrics, diagnostics, and regularization.

### Instructor notes

Require the regression/classification distinction before code and verify one prediction and one residual manually.

### Notebook connection

Continue into `03.model-development.ipynb`, then use the regression sections of `04.model-evaluation-techniques.ipynb`.

### Sources

- [AI Bootcamp: Model Development](https://github.com/curiousily/AI-Bootcamp/blob/master/03.model-development.ipynb)
- [AI Bootcamp: Model Evaluation Techniques](https://github.com/curiousily/AI-Bootcamp/blob/master/04.model-evaluation-techniques.ipynb)
