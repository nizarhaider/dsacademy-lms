# Week 5: Mathematics and Statistics for Machine Learning

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners comfortable with arithmetic, arrays, and averages  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 5 presentation and related media.

---

## Slide 1 - A Function Maps an Input to an Output

### Teaching purpose

Connect familiar calculations to the mathematical idea of a function.

### Learner-facing content

A mathematical **function** is a rule that maps each allowed input to one output.

`y = f(x)`

- `x` is the input.
- `f` is the rule.
- `y` is the output.

For `f(x) = 2x + 1`, the coefficient `2` controls how quickly output changes and the intercept `1` is the output when `x = 0`.

Machine-learning models are functions whose parameters are estimated from data.

### Worked example

For `f(x) = 2x + 1` and `x = 3`:

1. Multiply: `2 x 3 = 6`
2. Add intercept: `6 + 1 = 7`
3. Therefore `f(3) = 7`

### Code example

```python
def f(x):
    return 2 * x + 1

print(f(3))
```

Expected output:

```text
7
```

### Visual description

An input `3` passes through a box labelled `multiply by 2, then add 1` and becomes `7`. A line graph marks `(0,1)` and `(3,7)`.

### Instructor notes

Connect this to Python functions but distinguish a mathematical mapping from Python syntax.

### Notebook connection

Later model equations use the same input-rule-output structure with learned parameters.

### Sources

- [Mathematics for Machine Learning](https://mml-book.github.io/)
- [OpenStax: Functions](https://openstax.org/books/college-algebra-2e/pages/3-1-functions-and-function-notation)

---

## Slide 2 - Slope Measures Change

### Teaching purpose

Define slope before derivatives, gradients, and linear regression.

### Learner-facing content

The **slope** of a straight line measures output change per unit of input change.

`slope = change in y / change in x = Δy / Δx`

A positive slope rises, a negative slope falls, and zero slope is horizontal. Slope has units: if `x` is hours and `y` is kilometres, slope is kilometres per hour.

### Worked example

Two points are `(1, 3)` and `(4, 9)`.

`Δy = 9 - 3 = 6`  
`Δx = 4 - 1 = 3`  
`slope = 6 / 3 = 2`

For every one-unit increase in `x`, `y` increases by `2`.

### Code example

```python
x1, y1 = 1, 3
x2, y2 = 4, 9
slope = (y2 - y1) / (x2 - x1)
print(slope)
```

Expected output:

```text
2.0
```

### Visual description

A coordinate plane shows the two points and a right triangle labelled `run = 3`, `rise = 6`, and slope `2`.

### Instructor notes

Always state units and direction. Explain that division by zero occurs for a vertical line.

### Notebook connection

Slope becomes a coefficient in Week 7 and local slope becomes a derivative later this week.

### Sources

- [OpenStax: Linear Functions](https://openstax.org/books/college-algebra-2e/pages/2-1-linear-functions)
- [Mathematics for Machine Learning: Linear Algebra](https://mml-book.github.io/book/mml-book.pdf)

---

## Slide 3 - Vectors Represent Several Features Together

### Teaching purpose

Define vectors as ordered numerical representations.

### Learner-facing content

A **vector** is an ordered list of numbers.

`x = [x1, x2, ..., xn]`

In machine learning, one vector can represent one observation. Each position has a fixed meaning.

Example:

`x = [5, 3, 8]`

could mean `5` study hours, `3` assignments, and `8` hours of sleep. Reordering values without reordering their meanings creates incorrect data.

### Worked example

Add vectors position by position:

`[2, 4] + [1, 3] = [2+1, 4+3] = [3, 7]`

Multiply by a scalar:

`2[3, 7] = [6, 14]`

### Code example

```python
import numpy as np

a = np.array([2, 4])
b = np.array([1, 3])
print(a + b)
```

Expected output:

```text
[3 7]
```

### Visual description

A student record becomes a three-position vector with feature names aligned above each position.

### Instructor notes

Stress order and units. Avoid introducing abstract vector spaces; the goal is model-ready representation.

### Notebook connection

NumPy arrays and PyTorch tensors later store batches of feature vectors.

### Sources

- [Mathematics for Machine Learning: Vectors](https://mml-book.github.io/book/mml-book.pdf)
- [NumPy: Array Objects](https://numpy.org/doc/stable/reference/arrays.html)

---

## Slide 4 - Matrices Stack Observations into Rows

### Teaching purpose

Define matrices and shape compatibility.

### Learner-facing content

A **matrix** is a rectangular grid of numbers. A dataset matrix commonly uses:

- one row per observation;
- one column per feature.

`X` with shape `(m, n)` contains `m` observations and `n` features.

Matrix multiplication is valid when inner dimensions match:

`(m, n) @ (n, p) -> (m, p)`

The shared `n` means both operands refer to the same number of features.

### Worked example

`X` has shape `(3, 2)`: three students, two features.  
`w` has shape `(2, 1)`: one weight for each feature.

`X @ w` has shape `(3, 1)`: one result for each student.

### Code example

```python
X = np.array([[2, 1], [3, 4], [5, 2]])
w = np.array([[0.5], [2.0]])
print((X @ w).shape)
```

Expected output:

```text
(3, 1)
```

### Visual description

Shape blocks `(3,2)` and `(2,1)` align at the shared `2`; the result block is `(3,1)`.

### Instructor notes

Check shapes before values. Have learners say what every dimension represents.

### Notebook connection

This prepares learners for matrix-shaped batches and weight matrices in neural networks.

### Sources

- [Mathematics for Machine Learning: Matrices](https://mml-book.github.io/book/mml-book.pdf)
- [NumPy: Matrix Products](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)

---

## Slide 5 - A Dot Product Produces a Weighted Sum

### Teaching purpose

Explain the central operation used by linear models and neurons.

### Learner-facing content

The **dot product** multiplies matching vector positions and adds the products:

`x · w = x1w1 + x2w2 + ... + xnwn`

In a model, `x` contains feature values and `w` contains one weight for each feature. A larger positive weight increases the result when its feature increases; a negative weight decreases it.

### Worked example

`x = [2, 3]` and `w = [0.4, -0.1]`

`x · w = (2 x 0.4) + (3 x -0.1)`  
`= 0.8 - 0.3`  
`= 0.5`

With intercept `b = 0.2`, prediction is `0.5 + 0.2 = 0.7`.

### Code example

```python
x = np.array([2.0, 3.0])
w = np.array([0.4, -0.1])
prediction = x @ w + 0.2
print(prediction)
```

Expected output:

```text
0.7
```

### Visual description

Matching feature and weight pairs are multiplied, then arrows merge into a sum and intercept.

### Instructor notes

Work every multiplication separately. Explain that the dot product is one number, not another same-length vector.

### Notebook connection

Week 7 linear regression and Week 9 neurons both use weighted sums.

### Sources

- [Mathematics for Machine Learning: Inner Products](https://mml-book.github.io/book/mml-book.pdf)
- [NumPy: numpy.dot](https://numpy.org/doc/stable/reference/generated/numpy.dot.html)

---

## Slide 6 - Variance Measures Squared Distance from the Mean

### Teaching purpose

Connect descriptive spread to error functions.

### Learner-facing content

For values `x1 ... xn` with mean `μ`, population variance is:

`variance = Σ(xi - μ)^2 / n`

- `xi`: one value
- `μ`: mean
- `xi - μ`: deviation from the mean
- squaring makes deviations non-negative and emphasizes large distances
- `Σ` means add all terms
- dividing by `n` gives the average squared deviation

Standard deviation is `sqrt(variance)` and returns to the original units.

### Worked example

For `[2, 4, 6]`, mean is `4`.

Deviations: `[-2, 0, 2]`  
Squared: `[4, 0, 4]`  
Variance: `8 / 3 = 2.67`  
Standard deviation: `sqrt(2.67) = 1.63`

### Code example

```python
values = np.array([2, 4, 6])
print(values.var(), values.std())
```

Expected output:

```text
2.6666666666666665 1.632993161855452
```

### Visual description

A four-row calculation table shows value, deviation, squared deviation, and total.

### Instructor notes

Link squared deviation to squared prediction error but distinguish spread around the mean from model loss.

### Notebook connection

The same subtract-square-average pattern appears in mean squared error.

### Sources

- [NIST: Variance](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3561.htm)
- [NumPy: numpy.var](https://numpy.org/doc/stable/reference/generated/numpy.var.html)

---

## Slide 7 - Probability Represents Uncertainty

### Teaching purpose

Introduce probability as a number between zero and one.

### Learner-facing content

A **probability** describes uncertainty about an event.

`0 <= P(event) <= 1`

- `0` means impossible under the model.
- `1` means certain under the model.
- `0.25` means a 25% probability.

For equally likely outcomes:

`P(event) = favourable outcomes / possible outcomes`

Observed frequency can estimate probability, but an estimate depends on sample size and whether the data represents future cases.

### Worked example

A bag contains `3` blue and `1` red token.

Total outcomes: `4`  
Favourable blue outcomes: `3`  
`P(blue) = 3 / 4 = 0.75`

### Code example

```python
blue = 3
total = 4
print(blue / total)
```

Expected output:

```text
0.75
```

### Visual description

Four equal token icons show three blue and one red, paired with fraction, decimal, and percentage representations.

### Instructor notes

State assumptions such as equal chance of drawing each token. Avoid presenting model probabilities as guaranteed frequencies for an individual.

### Notebook connection

Classification models later output class probabilities that are converted into decisions.

### Sources

- [OpenStax: Probability Topics](https://openstax.org/books/introductory-statistics-2e/pages/3-introduction)
- [Scikit-learn: Probability Calibration](https://scikit-learn.org/stable/modules/calibration.html)

---

## Slide 8 - A Derivative Is Local Slope

### Teaching purpose

Give an intuitive definition of derivatives before gradients.

### Learner-facing content

A **derivative** measures how quickly a function changes near one input. It is the slope of the tangent line at that point.

For `f(x) = x^2`, the derivative is:

`f'(x) = 2x`

At `x = 3`, the local slope is `2 x 3 = 6`. Near `x = 3`, a small increase of `0.1` in `x` changes `f(x)` by approximately `6 x 0.1 = 0.6`.

### Worked example

Exact values:

`f(3) = 9`  
`f(3.1) = 9.61`  
Actual change: `0.61`

Derivative estimate: `6 x 0.1 = 0.6`, which is close for a small step.

### Code example

```python
def f(x):
    return x**2

approx_slope = (f(3.001) - f(3)) / 0.001
print(round(approx_slope, 3))
```

Expected output:

```text
6.001
```

### Visual description

A curve `y=x²` has a tangent line at `x=3`; a small horizontal step and corresponding vertical change are marked.

### Instructor notes

Use “local slope” consistently. Do not derive limits formally in this beginner lesson.

### Notebook connection

Optimization uses derivatives of loss with respect to model parameters.

### Sources

- [OpenStax Calculus: Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative)
- [Mathematics for Machine Learning: Vector Calculus](https://mml-book.github.io/book/mml-book.pdf)

---

## Slide 9 - A Gradient Collects One Slope per Parameter

### Teaching purpose

Extend a derivative from one parameter to several.

### Learner-facing content

A **parameter** is a value a model adjusts during training. When loss depends on several parameters, the **gradient** collects one partial derivative for each parameter:

`∇L = [∂L/∂w1, ∂L/∂w2, ...]`

- `L`: loss
- `wi`: one parameter
- `∂L/∂wi`: local change in loss when only that parameter changes
- `∇L`: direction of fastest local increase in loss

Moving opposite the gradient reduces loss for a sufficiently small step.

### Worked example

If `∇L = [2, -3]`:

- increasing `w1` increases loss locally, so reduce `w1`;
- increasing `w2` decreases loss locally, so increase `w2`.

The opposite direction is `[-2, 3]`.

### Code example

```python
gradient = np.array([2.0, -3.0])
descent_direction = -gradient
print(descent_direction)
```

Expected output:

```text
[-2.  3.]
```

### Visual description

A contour map shows a point, a gradient arrow uphill, and a descent arrow in the opposite direction.

### Instructor notes

Do not say the gradient “points to the minimum.” It points uphill locally; its negative points downhill locally.

### Notebook connection

PyTorch later computes gradients automatically during backpropagation.

### Sources

- [Mathematics for Machine Learning: Gradients](https://mml-book.github.io/book/mml-book.pdf)
- [PyTorch: Autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

---

## Slide 10 - Loss Measures Prediction Error

### Teaching purpose

Define loss and mean squared error with every symbol explained.

### Learner-facing content

A **loss function** converts prediction error into a number that training can reduce.

Mean squared error:

`MSE = (1/n) Σ(yi - ŷi)^2`

- `n`: number of examples
- `yi`: actual target for example `i`
- `ŷi`: predicted target
- `yi - ŷi`: residual
- squaring removes signs and emphasizes large errors
- mean gives one summary across examples

Lower MSE means predictions are closer under this squared-error rule.

### Worked example

Actual `[3, 5]`, predicted `[2, 7]`

Residuals: `[1, -2]`  
Squared residuals: `[1, 4]`  
`MSE = (1 + 4) / 2 = 2.5`

### Code example

```python
actual = np.array([3, 5])
predicted = np.array([2, 7])
mse = np.mean((actual - predicted) ** 2)
print(mse)
```

Expected output:

```text
2.5
```

### Visual description

A table shows actual, predicted, residual, squared residual, sum, and mean.

### Instructor notes

Explain that choosing a loss expresses which errors receive more weight. MSE is not suitable for every problem.

### Notebook connection

Linear regression and neural networks train by minimizing a loss.

### Sources

- [Scikit-learn: Mean Squared Error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
- [Mathematics for Machine Learning: Optimization](https://mml-book.github.io/book/mml-book.pdf)

---

## Slide 11 - Gradient Descent Updates Parameters Step by Step

### Teaching purpose

Explain the update equation and perform one numerical update.

### Learner-facing content

**Gradient descent** repeatedly adjusts parameters in the direction that locally reduces loss:

`w_new = w_old - η ∂L/∂w`

- `w_old`: current parameter
- `∂L/∂w`: current loss slope
- `η` (eta): learning rate
- subtraction moves opposite the gradient
- `w_new`: updated parameter

A learning rate that is too large can overshoot; one that is too small can make progress slow.

### Worked example

`w_old = 0.5`, gradient `= 4`, learning rate `η = 0.1`

`w_new = 0.5 - 0.1 x 4`  
`= 0.5 - 0.4`  
`= 0.1`

### Code example

```python
w = 0.5
gradient = 4.0
learning_rate = 0.1
w = w - learning_rate * gradient
print(w)
```

Expected output:

```text
0.09999999999999998
```

### Visual description

A loss curve shows one step downhill. A side panel expands the update equation into values and intermediate steps.

### Instructor notes

Explain the small floating-point display difference. Emphasize that training recomputes the gradient after each update.

### Notebook connection

Week 9's optimizer performs this update across many neural-network parameters.

### Sources

- [Dive into Deep Learning: Gradient Descent](https://d2l.ai/chapter_optimization/gd.html)
- [PyTorch: Optimizing Model Parameters](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)

---

## Slide 12 - Guided Lab: Match Hand Calculations to NumPy

### Teaching purpose

Set the mathematical readiness check for machine-learning fundamentals.

### Learner-facing content

Complete and explain:

1. vector shape and matrix shape;
2. one dot product;
3. one mean and population variance;
4. one probability;
5. one squared-error calculation;
6. one gradient-descent update.

For every calculation, show intermediate values by hand and then confirm them with NumPy. A matching number is not enough; state what the number means and which units it uses.

### Worked example

For `x=[2,3]`, `w=[0.4,-0.1]`, `b=0.2`, and target `1`:

Prediction `= 0.7`  
Residual `= 1 - 0.7 = 0.3`  
Squared error `= 0.3² = 0.09`

### Code example

```python
prediction = x @ w + 0.2
squared_error = (1 - prediction) ** 2
print(prediction, squared_error)
```

Expected output:

```text
0.7 0.09000000000000002
```

### Visual description

A readiness checklist connects shapes, weighted sum, residual, loss, gradient, and update.

### Instructor notes

Require learners to predict each result before execution and explain floating-point approximations.

### Notebook connection

These concepts prepare learners to read model equations and training loops in later notebooks.

### Sources

- [Mathematics for Machine Learning](https://mml-book.github.io/)
- [NumPy User Guide](https://numpy.org/doc/stable/user/)
