# Week 9: Neural Networks and PyTorch

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who understand weighted sums, loss, gradients, and evaluation  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 9 presentation and related media.

---

## Slide 1 - Tensors Store Model Data and Parameters

### Teaching purpose

Connect NumPy arrays to PyTorch tensors.

### Learner-facing content

A PyTorch **tensor** is a shaped numerical data structure used for inputs, targets, model parameters, and intermediate results.

Like a NumPy array, a tensor has:

- `shape`: length of each axis;
- `dtype`: stored numerical type;
- `device`: CPU, GPU, or another accelerator;
- values selected by indexing.

PyTorch tensors can record operations for automatic gradient calculation.

### Worked example

A batch contains `4` students and `3` features per student.

Input shape: `(4, 3)`  
If the model predicts one value per student, output shape: `(4, 1)`.

### Code example

```python
import torch

x = torch.tensor([[2.0, 3.0], [4.0, 1.0]])
print(x.shape, x.dtype, x.device)
```

Expected output:

```text
torch.Size([2, 2]) torch.float32 cpu
```

### Visual description

A NumPy-style grid gains shape, dtype, device, and gradient-history labels to become a tensor.

### Instructor notes

Have learners predict every shape. Explain that exact device output depends on where the tensor was created.

### Notebook connection

The PyTorch notebook starts with tensor creation, operations, and device movement.

### Sources

- [PyTorch: Tensors](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
- [AI Bootcamp: Real-world PyTorch](https://github.com/curiousily/AI-Bootcamp/blob/master/02.real-world-pytorch.ipynb)

---

## Slide 2 - One Neuron Is a Weighted Sum and Activation

### Teaching purpose

Define the smallest neural-network unit using familiar mathematics.

### Learner-facing content

A **neuron** calculates:

`z = w1x1 + w2x2 + ... + wnxn + b`

then applies an **activation function**:

`a = g(z)`

- `xi`: input feature
- `wi`: learned weight
- `b`: learned bias
- `z`: pre-activation weighted sum
- `g`: activation function
- `a`: neuron output

The bias has the same role as a regression intercept.

### Worked example

`x=[2,3]`, `w=[0.4,-0.1]`, `b=0.2`

`z = 2(0.4) + 3(-0.1) + 0.2`  
`= 0.8 - 0.3 + 0.2 = 0.7`

If `g` is ReLU, output remains `0.7`.

### Code example

```python
x = torch.tensor([2.0, 3.0])
w = torch.tensor([0.4, -0.1])
z = x @ w + 0.2
print(z)
```

Expected output:

```text
tensor(0.7000)
```

### Visual description

Two feature-weight pairs merge into a sum with bias, then pass through an activation block.

### Instructor notes

Connect each term to Week 5's dot product and Week 7's linear equation.

### Notebook connection

PyTorch `nn.Linear` performs the weighted sum and bias for a complete layer.

### Sources

- [PyTorch: Building the Neural Network](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
- [Dive into Deep Learning: Multilayer Perceptrons](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)

---

## Slide 3 - Layers Transform Batches with Matrix Multiplication

### Teaching purpose

Explain layer shapes before learners instantiate modules.

### Learner-facing content

A **layer** contains several neurons that receive the same input vector.

For a batch:

`Z = XWᵀ + b`

If:

- `X` shape is `(batch, input_features)`;
- `W` shape is `(output_features, input_features)`;
- then `Z` shape is `(batch, output_features)`.

Each output column comes from one neuron's weights.

### Worked example

Batch `X`: `(4, 3)`  
Layer: `3` inputs to `5` outputs  
Weight `W`: `(5, 3)`  
Output `Z`: `(4, 5)`

Four observations each receive five transformed features.

### Code example

```python
layer = torch.nn.Linear(3, 5)
x = torch.randn(4, 3)
z = layer(x)
print(z.shape)
```

Expected output:

```text
torch.Size([4, 5])
```

### Visual description

A `(4,3)` batch matrix connects to a 3-to-5 layer and becomes a `(4,5)` output matrix.

### Instructor notes

Ask what every dimension means. Explain that `nn.Linear(3,5)` refers to features, not batch size.

### Notebook connection

The model section constructs layers whose dimensions must match dataset tensors.

### Sources

- [PyTorch: nn.Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)
- [PyTorch: Build Model](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)

---

## Slide 4 - Activations Let Networks Learn Nonlinear Patterns

### Teaching purpose

Explain why stacked linear layers alone are insufficient.

### Learner-facing content

An **activation function** transforms each pre-activation value.

ReLU:

`ReLU(z) = max(0, z)`

Without nonlinear activations, several linear layers collapse into one linear transformation. Nonlinearity lets the network represent curved and piecewise relationships.

Common output activations depend on the task. PyTorch loss functions often expect raw logits, so do not add sigmoid or softmax blindly.

### Worked example

Input values `[-2, 0.5, 3]`

ReLU:

`max(0,-2)=0`  
`max(0,0.5)=0.5`  
`max(0,3)=3`

Output `[0, 0.5, 3]`.

### Code example

```python
values = torch.tensor([-2.0, 0.5, 3.0])
print(torch.relu(values))
```

Expected output:

```text
tensor([0.0000, 0.5000, 3.0000])
```

### Visual description

A ReLU graph is paired with three input arrows and their transformed outputs.

### Instructor notes

Avoid surveying many activations. Focus on the role of nonlinearity and the loss-output contract.

### Notebook connection

Learners should identify every activation and the shape it preserves.

### Sources

- [PyTorch: ReLU](https://docs.pytorch.org/docs/stable/generated/torch.nn.ReLU.html)
- [Dive into Deep Learning: Activation Functions](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html#activation-functions)

---

## Slide 5 - A Forward Pass Produces Predictions

### Teaching purpose

Define the ordered computation from batch input to output.

### Learner-facing content

A **forward pass** sends input tensors through layers and activations to produce predictions.

Example network:

`X -> Linear(3,5) -> ReLU -> Linear(5,1) -> output`

The output of one stage becomes the input to the next. Shapes must align at every boundary.

The final output may be a regression prediction, a binary logit, or one logit per class.

### Worked example

Batch shape `(4,3)`

After first linear layer: `(4,5)`  
After ReLU: `(4,5)`  
After output layer: `(4,1)`

There is one raw output per observation.

### Code example

```python
model = torch.nn.Sequential(
    torch.nn.Linear(3, 5),
    torch.nn.ReLU(),
    torch.nn.Linear(5, 1),
)
print(model(torch.randn(4, 3)).shape)
```

Expected output:

```text
torch.Size([4, 1])
```

### Visual description

A left-to-right network pipeline labels each layer and tensor shape.

### Instructor notes

Trace shape changes before discussing learning. The forward pass alone does not update parameters.

### Notebook connection

The notebook's model call executes `forward()` and returns a tensor for the loss function.

### Sources

- [PyTorch: Sequential](https://docs.pytorch.org/docs/stable/generated/torch.nn.Sequential.html)
- [PyTorch: Build Model](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)

---

## Slide 6 - The Loss Must Match the Task and Output

### Teaching purpose

Connect model outputs to task-specific training objectives.

### Learner-facing content

A **loss function** compares model outputs with targets and returns a value training will reduce.

- Regression: mean squared error can compare numerical predictions and targets.
- Binary classification: `BCEWithLogitsLoss` combines sigmoid and binary cross-entropy safely.
- Multiclass classification: `CrossEntropyLoss` expects one raw logit per class and integer class labels.

Using the wrong target shape, target type, or extra activation can produce errors or incorrect learning.

### Worked example

Regression predictions `[2,4]`, targets `[3,5]`

Residuals `[1,1]`  
Squared residuals `[1,1]`  
MSE `(1+1)/2 = 1`

### Code example

```python
loss_fn = torch.nn.MSELoss()
prediction = torch.tensor([2.0, 4.0])
target = torch.tensor([3.0, 5.0])
print(loss_fn(prediction, target))
```

Expected output:

```text
tensor(1.)
```

### Visual description

Three task lanes map model output, target format, and matching loss.

### Instructor notes

Explain logits as raw scores. Keep probability conversion for evaluation separate from loss input.

### Notebook connection

Learners must explain why the notebook's chosen loss matches its prediction task.

### Sources

- [PyTorch: Loss Functions](https://docs.pytorch.org/docs/stable/nn.html#loss-functions)
- [PyTorch: BCEWithLogitsLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)

---

## Slide 7 - Backpropagation Computes Gradients

### Teaching purpose

Explain automatic differentiation and the backward pass.

### Learner-facing content

PyTorch **autograd** records tensor operations in a computational graph.

During **backpropagation**, the chain rule moves backward from loss and calculates:

`∂loss / ∂parameter`

for every trainable parameter.

Calling `loss.backward()` computes gradients. It does not update the weights. Gradients are stored in each parameter's `.grad`.

### Worked example

`prediction = wx`, target `y`, squared loss `(y - wx)^2`.

If `x=2`, `w=1`, `y=5`:

Prediction `2`; residual `3`; loss `9`.  
Derivative with respect to `w`: `-2x(y-wx) = -12`.

Increasing `w` should reduce loss.

### Code example

```python
w = torch.tensor(1.0, requires_grad=True)
loss = (5 - w * 2) ** 2
loss.backward()
print(w.grad)
```

Expected output:

```text
tensor(-12.)
```

### Visual description

A forward graph calculates prediction and loss; a backward arrow carries gradients to `w`.

### Instructor notes

Separate gradient computation from parameter update. Explain that gradients accumulate unless cleared.

### Notebook connection

The training loop calls `backward()` after calculating loss.

### Sources

- [PyTorch: Autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- [PyTorch: Fundamentals of Autograd](https://docs.pytorch.org/tutorials/beginner/introyt/autogradyt_tutorial.html)

---

## Slide 8 - The Optimizer Applies the Gradients

### Teaching purpose

Explain the four essential training-loop operations.

### Learner-facing content

For each training batch:

1. `optimizer.zero_grad()` clears old gradients;
2. `prediction = model(x)` runs the forward pass;
3. `loss.backward()` computes new gradients;
4. `optimizer.step()` updates parameters.

The **optimizer** implements the update rule. Stochastic gradient descent and Adam are common choices. The **learning rate** controls update size.

### Worked example

Current weight `1.0`, gradient `-12`, learning rate `0.1`:

`w_new = 1.0 - 0.1(-12)`  
`= 2.2`

For the example on Slide 7, this moves the prediction from `2` toward target `5`.

### Code example

```python
optimizer.zero_grad()
prediction = model(x)
loss = loss_fn(prediction, y)
loss.backward()
optimizer.step()
```

Expected output:

```text
Parameters are updated once using gradients from the current batch.
```

### Visual description

A four-step loop labels clear, forward, backward, and update, with parameter state before and after.

### Instructor notes

Ask what breaks if `zero_grad()` is omitted. Do not teach Adam internals in this lesson.

### Notebook connection

This sequence is the core of the notebook training section.

### Sources

- [PyTorch: Optimization Loop](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [PyTorch: Optimizers](https://docs.pytorch.org/docs/stable/optim.html)

---

## Slide 9 - Batches, Epochs, and Learning Rate Control Training

### Teaching purpose

Define the main training units and their tradeoffs.

### Learner-facing content

A **batch** is a subset of training observations used for one gradient update.

An **epoch** is one complete pass through the training dataset.

If there are `1,000` rows and batch size is `100`, one epoch contains `10` batches and usually `10` optimizer updates.

Smaller batches use less memory and produce noisier gradient estimates. Larger batches use more memory. More epochs do not guarantee better generalization.

### Worked example

Dataset size `240`, batch size `32`.

Seven full batches contain `224` rows, plus one final batch of `16`.  
Updates per epoch: `ceil(240/32) = 8`.

For `5` epochs: `8 x 5 = 40` updates.

### Code example

```python
import math

updates = math.ceil(240 / 32) * 5
print(updates)
```

Expected output:

```text
40
```

### Visual description

A dataset bar splits into batches, which group into one epoch; several epochs appear on a training timeline.

### Instructor notes

Distinguish an epoch from an update. Connect learning rate to update size, not number of passes.

### Notebook connection

Learners should calculate expected batches and explain logged loss frequency.

### Sources

- [PyTorch: Datasets and DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
- [PyTorch: Optimization](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)

---

## Slide 10 - Training and Evaluation Modes Behave Differently

### Teaching purpose

Teach correct validation behaviour and device consistency.

### Learner-facing content

`model.train()` enables training-time behaviour.  
`model.eval()` enables evaluation-time behaviour for layers such as dropout and batch normalization.

During evaluation, use `torch.inference_mode()` or `torch.no_grad()` to avoid storing gradients.

The model and all input tensors must be on compatible devices. Moving only the model or only the data causes a device mismatch.

### Worked example

Correct evaluation sequence:

1. `model.eval()`
2. enter `torch.inference_mode()`
3. move batch to the model device
4. calculate predictions and metrics
5. do not call optimizer methods

### Code example

```python
model.eval()
with torch.inference_mode():
    predictions = model(x_valid)
```

Expected output:

```text
Validation predictions without gradient tracking or parameter updates.
```

### Visual description

Training and evaluation lanes show mode, gradient tracking, parameter update, and data-device rules.

### Instructor notes

Explain that `eval()` does not disable gradients by itself and inference mode does not set evaluation behaviour by itself.

### Notebook connection

The notebook evaluation section must use both correct model mode and no-gradient execution.

### Sources

- [PyTorch: Module.eval](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval)
- [PyTorch: inference_mode](https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad_mode.inference_mode.html)

---

## Slide 11 - A Complete Training Loop Produces Evidence

### Teaching purpose

Assemble the mechanisms into a readable loop.

### Learner-facing content

A training loop should expose:

- input and target shapes;
- forward output shape;
- loss value;
- gradient calculation;
- parameter update;
- training and validation metrics by epoch;
- random seed and device;
- saved best model based on validation evidence.

Training loss alone does not establish generalization. Validation must run without updates.

### Worked example

If training loss falls from `1.2` to `0.1` while validation loss falls to `0.4` then rises to `0.9`, later epochs may be overfitting.

The preferred checkpoint is near the lowest validation loss, not automatically the final epoch.

### Code example

```python
for x, y in train_loader:
    optimizer.zero_grad()
    prediction = model(x)
    loss = loss_fn(prediction, y)
    loss.backward()
    optimizer.step()
```

Expected output:

```text
One parameter update per batch; epoch metrics are logged separately.
```

### Visual description

An epoch chart shows training and validation loss diverging after the best checkpoint.

### Instructor notes

Trace one batch line by line before showing the full loop. Require validation outside the update loop.

### Notebook connection

This maps directly to the real-world PyTorch notebook's model, training, and evaluation sections.

### Sources

- [PyTorch: Optimizing Model Parameters](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [AI Bootcamp: Real-world PyTorch](https://github.com/curiousily/AI-Bootcamp/blob/master/02.real-world-pytorch.ipynb)

---

## Slide 12 - Guided Lab: Trace One Batch End to End

### Teaching purpose

Set a concrete PyTorch notebook-readiness assessment.

### Learner-facing content

Build a small network and document:

1. input and target tensor shapes;
2. device and dtype;
3. every layer's input and output shape;
4. weighted sum and activation for one simple neuron;
5. matching task and loss;
6. one forward loss value;
7. one parameter gradient after `backward()`;
8. one parameter value before and after `step()`;
9. batch count and epoch count;
10. validation in evaluation and inference modes.

### Worked example

For `240` rows, batch `32`, and `5` epochs:

`8` batches per epoch and `40` updates. A validation pass performs `0` updates.

### Code example

```python
before = next(model.parameters()).detach().clone()
loss.backward()
optimizer.step()
after = next(model.parameters()).detach().clone()
print(torch.equal(before, after))
```

Expected output:

```text
False
```

### Visual description

A trace sheet follows one batch from data loader through forward pass, loss, gradients, update, and validation.

### Instructor notes

Require learners to inspect one parameter rather than claiming “the model learned” from loss output alone.

### Notebook connection

Complete `02.real-world-pytorch.ipynb`, predicting shapes and state changes before each section.

### Sources

- [AI Bootcamp: Real-world PyTorch](https://github.com/curiousily/AI-Bootcamp/blob/master/02.real-world-pytorch.ipynb)
- [PyTorch: Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/)
