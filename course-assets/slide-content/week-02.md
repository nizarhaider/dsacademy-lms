# Week 2: Python Data Structures and Program Logic

**Status:** PRODUCTION AUTHORIZED

**Audience:** Complete beginners who have completed Week 1  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 2 presentation and related media.

---

## Slide 1 - Programs Need Collections and Decisions

### Teaching purpose

Connect Week 1's individual values to programs that handle multiple values and choose or repeat actions.

### Learner-facing content

In Week 1, one variable stored one value:

```python
visitors_today = 120
```

Real programs usually need to:

- store several related values;
- find or update one value;
- choose an action using a condition;
- repeat an action for multiple values; and
- reuse a solution without rewriting it.

A **data structure** organizes related values. **Program logic** controls which statements run and how often they run.

This week combines both ideas. Collections hold the data; conditions, loops, and functions describe what the program does with it.

### Worked example

Suppose a museum records visitor counts for three days:

```text
Monday: 120
Tuesday: 135
Wednesday: 128
```

Three separate variables work, but they become difficult to process together. A list stores the three counts as one collection:

```python
visitor_counts = [120, 135, 128]
```

### Code example

```python
visitor_counts = [120, 135, 128]

print(len(visitor_counts))
print(sum(visitor_counts))
```

Expected output:

```text
3
383
```

### Visual description

Three disconnected variable boxes transform into one labelled list containing three ordered values. Arrows then connect the list to `len()` and `sum()`.

### Instructor notes

- Recap values, variables, assignment, and function calls from Week 1.
- Explain that a collection is still one Python value, but it contains other values.
- Preview the lesson sequence: store, select, repeat, and reuse.

### Notebook connection

The notebook begins with collections used for model features, importance values, labels, and data points. This slide establishes why those collections are needed.

### Sources

- [Python Tutorial: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Slide 2 - Lists Store an Ordered Sequence

### Teaching purpose

Define lists, indexing, length, and slicing using a traceable example.

### Learner-facing content

A **list** is an ordered, changeable collection of values.

```python
visitor_counts = [120, 135, 128]
```

Each value is an **element**. Its position is its **index**.

Python starts indexing at zero:

| Index | `0` | `1` | `2` |
|---|---:|---:|---:|
| Value | `120` | `135` | `128` |

Square brackets select an element:

```python
visitor_counts[1]
```

This produces `135`, because index `1` means the second element.

A **slice** selects a range. The ending index is not included.

### Worked example

For `[120, 135, 128]`:

1. `visitor_counts[0]` gives the first value: `120`.
2. `visitor_counts[2]` gives the third value: `128`.
3. `visitor_counts[-1]` gives the final value: `128`.
4. `visitor_counts[0:2]` gives indexes `0` and `1`: `[120, 135]`.
5. `len(visitor_counts)` gives the number of elements: `3`.

### Code example

```python
visitor_counts = [120, 135, 128]

print(visitor_counts[0])
print(visitor_counts[-1])
print(visitor_counts[0:2])
```

Expected output:

```text
120
128
[120, 135]
```

### Visual description

A three-cell list is shown with indexes above and values below. Brackets highlight index `1`, then a wider bracket highlights the slice from `0` up to, but not including, `2`.

### Instructor notes

- Count positions aloud from zero.
- Contrast an index with the value stored at that index.
- Demonstrate that an invalid index produces `IndexError`.

### Notebook connection

Learners can now read `model_features = ["age", "income", "education_level"]` and select individual feature names.

### Sources

- [Python Tutorial: Lists](https://docs.python.org/3/tutorial/introduction.html#lists)
- [Python Tutorial: More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

---

## Slide 3 - Lists Can Be Changed

### Teaching purpose

Teach mutability and the basic list operations used in the notebook.

### Learner-facing content

A list is **mutable**, meaning its contents can change after the list is created.

Common operations are:

- `append(value)`: add one value to the end;
- `list[index] = value`: replace an element;
- `remove(value)`: remove the first matching value; and
- `pop()`: remove and return an element.

Methods such as `append()` change the existing list. They do not create a second list.

For data work, lists are useful when the number of items may grow or when values need to be corrected.

### Worked example

Start with:

```python
model_features = ["age", "income"]
```

1. Append `"education"` -> `["age", "income", "education"]`
2. Replace index `1` with `"monthly_income"` -> `["age", "monthly_income", "education"]`
3. Remove `"age"` -> `["monthly_income", "education"]`

The same variable still refers to the changed list.

### Code example

```python
model_features = ["age", "income"]

model_features.append("education")
model_features[1] = "monthly_income"

print(model_features)
```

Expected output:

```text
['age', 'monthly_income', 'education']
```

### Visual description

One list changes across three states. A stable label `model_features` remains above it while elements are added and replaced.

### Instructor notes

- Link mutability to Week 1 reassignment, but distinguish changing a list from assigning a new list.
- Run the code one line at a time and inspect the list after each operation.
- Warn that `append()` adds one element; it does not sort the list.

### Notebook connection

This directly prepares learners for the notebook cell that appends `"marital_status"` to `model_features`.

### Sources

- [Python Tutorial: List Methods](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Slide 4 - Dictionaries Connect Keys to Values

### Teaching purpose

Explain key-value storage and lookup before the notebook uses feature dictionaries.

### Learner-facing content

A **dictionary** stores **key-value pairs**.

```python
feature_importance = {
    "age": 0.75,
    "income": 0.85
}
```

A **key** is the label used to find a value. Here `"age"` is a key and `0.75` is its value.

Unlike a list, a dictionary is not accessed by a position such as index `0`. It is accessed by a key:

```python
feature_importance["age"]
```

Dictionary keys must be unique. Assigning a new value to an existing key updates that pair.

### Worked example

Start with:

```python
scores = {"Asha": 85, "Ben": 72}
```

1. `scores["Asha"]` gives `85`.
2. `scores["Mina"] = 91` adds a new pair.
3. `scores["Ben"] = 78` updates Ben's value.
4. `"Mina" in scores` gives `True`.
5. `scores.get("Ravi", 0)` gives the default value `0` instead of raising `KeyError`.

### Code example

```python
scores = {"Asha": 85, "Ben": 72}

scores["Mina"] = 91
scores["Ben"] = 78

print(scores["Asha"])
print(scores.get("Ravi", 0))
```

Expected output:

```text
85
0
```

### Visual description

A two-column key-value map shows names on the left and scores on the right. A lookup arrow travels from `"Asha"` directly to `85`.

### Instructor notes

- Compare list indexes with dictionary keys.
- Explain that `{}` creates an empty dictionary.
- Demonstrate the difference between `dictionary[key]` and `dictionary.get(key, default)`.

### Notebook connection

Learners can now read the `feature_importance` and `data_point` dictionaries and understand lookup expressions such as `feature_importance["age"]`.

### Sources

- [Python Tutorial: Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Python Standard Types: Dictionaries](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)

---

## Slide 5 - Tuples Store a Fixed Ordered Record

### Teaching purpose

Distinguish tuples from lists and introduce packing, indexing, and unpacking.

### Learner-facing content

A **tuple** is an ordered collection that is usually used as one fixed record.

```python
result = ("Asha", 85)
```

Tuples use parentheses and support indexing:

```python
result[0]
```

A tuple is **immutable**, meaning its elements cannot be replaced after creation.

Tuples can be **unpacked** into separate variables:

```python
name, score = result
```

Unpacking requires the number of variables to match the number of tuple elements.

### Worked example

For `result = ("Asha", 85)`:

1. `result[0]` gives `"Asha"`.
2. `result[1]` gives `85`.
3. `name, score = result` assigns `"Asha"` to `name` and `85` to `score`.
4. `result[1] = 90` fails because the tuple is immutable.

Use a list when the collection should change. Use a tuple when the positions form one fixed record.

### Code example

```python
result = ("Asha", 85)
name, score = result

print(name)
print(score)
```

Expected output:

```text
Asha
85
```

### Visual description

A two-part record labelled `name` and `score` is packed into one tuple, then separates into two named variables through unpacking.

### Instructor notes

- Compare list brackets with tuple parentheses.
- Explain that immutable means the tuple's element positions cannot be reassigned.
- Avoid advanced exceptions involving mutable objects inside tuples.

### Notebook connection

The notebook stores one labelled data point as a tuple containing a feature dictionary and a class label. This slide teaches the outer tuple before learners inspect that nested value.

### Sources

- [Python Tutorial: Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Slide 6 - Sets Keep Unique Values

### Teaching purpose

Explain uniqueness, membership, and basic set operations.

### Learner-facing content

A **set** is an unordered collection with no duplicate elements.

```python
labels = {"spam", "not_spam"}
```

Sets are useful for:

- removing duplicate values;
- checking whether a value is present; and
- comparing groups.

Because a set is unordered, do not use an index such as `labels[0]`.

Important syntax:

- `{}` creates an empty dictionary.
- `set()` creates an empty set.

### Worked example

Start with repeated labels:

```python
predictions = ["spam", "spam", "not_spam", "spam"]
```

1. `set(predictions)` removes duplicates.
2. The result contains `"spam"` and `"not_spam"`.
3. `"spam" in unique_labels` gives `True`.
4. Adding `"spam"` again does not create a duplicate.

For two sets, `a & b` means values present in both sets.

### Code example

```python
predictions = ["spam", "spam", "not_spam", "spam"]
unique_labels = set(predictions)

unique_labels.add("spam")

print(len(unique_labels))
print("not_spam" in unique_labels)
```

Expected output:

```text
2
True
```

The printed order of set elements may vary.

### Visual description

A list containing four labels flows through `set()` into two unique label circles. A membership question points to a boolean result.

### Instructor notes

- Physically cross out duplicate labels in the example.
- Reinforce that membership does not depend on display order.
- Explain only intersection `&` as a preview; other set algebra can remain optional.

### Notebook connection

This prepares learners for `unique_labels = {"spam", "not_spam"}` and shows why adding `"spam"` again does not change the set.

### Sources

- [Python Tutorial: Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [Python Standard Types: Set Types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)

---

## Slide 7 - Conditions Choose Which Code Runs

### Teaching purpose

Teach `if`, `elif`, `else`, indentation, and mutually exclusive branches.

### Learner-facing content

A **condition** is an expression that produces `True` or `False`.

An `if` statement runs an indented block only when its condition is true:

```python
if score >= 70:
    print("Pass")
```

Python uses a colon and indentation to show which statements belong to a branch.

- `if` tests the first condition.
- `elif` tests another condition if earlier branches were false.
- `else` runs when no earlier branch matched.

Only the first matching branch in one `if`/`elif`/`else` chain runs.

### Worked example

For `score = 85`:

1. Test `score >= 90` -> `False`.
2. Test `score >= 70` -> `True`.
3. Print `"Pass"`.
4. Skip the remaining `else` branch.

For `score = 62`, both comparisons are false, so the result is `"Review"`.

### Code example

```python
score = 85

if score >= 90:
    result = "Excellent"
elif score >= 70:
    result = "Pass"
else:
    result = "Review"

print(result)
```

Expected output:

```text
Pass
```

### Visual description

A decision path tests `>= 90`, then `>= 70`, then reaches `else`. The path for score `85` is highlighted and ends at `Pass`.

### Instructor notes

- Ask learners to predict results for `95`, `85`, and `62`.
- Emphasize the colon and consistent indentation.
- Show that reversing the two conditions would make the broad condition catch high scores too early.

### Notebook connection

Conditions are required to complete the notebook's placeholder prediction function and to validate or classify values during later labs.

### Sources

- [Python Tutorial: if Statements](https://docs.python.org/3/tutorial/controlflow.html#if-statements)
- [Python Tutorial: More on Conditions](https://docs.python.org/3/tutorial/datastructures.html#more-on-conditions)

---

## Slide 8 - For Loops Process Each Element

### Teaching purpose

Explain iteration, the loop variable, indentation, and an accumulator.

### Learner-facing content

A **loop** repeats a block of code.

A `for` loop processes each element in a collection:

```python
for score in scores:
    print(score)
```

During each **iteration**, the loop variable `score` refers to the next element.

An **accumulator** is a variable that keeps a running result. It must be created before the loop and updated inside it.

The indented loop body runs once for every element.

### Worked example

For `scores = [72, 85, 90]`:

| Iteration | `score` | `total` after addition |
|---:|---:|---:|
| Start | - | `0` |
| 1 | `72` | `72` |
| 2 | `85` | `157` |
| 3 | `90` | `247` |

The loop ends after the final element. The total remains available after the loop.

### Code example

```python
scores = [72, 85, 90]
total = 0

for score in scores:
    total = total + score

print(total)
```

Expected output:

```text
247
```

### Visual description

A loop cursor moves across three list elements. Beside it, an accumulator meter changes from `0` to `72`, `157`, and `247`.

### Instructor notes

- Trace every iteration before running the code.
- Ask which lines run once and which line runs three times.
- Mention that `sum(scores)` is shorter, but the explicit loop reveals the mechanism.

### Notebook connection

Loops prepare learners to process feature names and values individually. They also provide the clear beginner equivalent of later `map()` examples.

### Sources

- [Python Tutorial: for Statements](https://docs.python.org/3/tutorial/controlflow.html#for-statements)
- [Python Tutorial: Looping Techniques](https://docs.python.org/3/tutorial/datastructures.html#looping-techniques)

---

## Slide 9 - While Loops Repeat While a Condition Is True

### Teaching purpose

Distinguish condition-controlled repetition from collection-controlled repetition.

### Learner-facing content

A `for` loop is suitable when processing items in a collection.

A `while` loop repeats while a condition remains `True`:

```python
while attempts < 3:
    attempts = attempts + 1
```

The condition is checked before every iteration.

Something inside the loop must eventually make the condition false. Otherwise, the program creates an **infinite loop** and does not stop normally.

Use `while` when the number of repetitions depends on a changing condition.

### Worked example

Start with `attempts = 0`:

1. `0 < 3` -> true; change attempts to `1`.
2. `1 < 3` -> true; change attempts to `2`.
3. `2 < 3` -> true; change attempts to `3`.
4. `3 < 3` -> false; stop.

The loop body runs three times.

### Code example

```python
attempts = 0

while attempts < 3:
    attempts = attempts + 1
    print(f"Attempt {attempts}")
```

Expected output:

```text
Attempt 1
Attempt 2
Attempt 3
```

### Visual description

A circular flow checks `attempts < 3`, runs the body, updates the counter, and returns to the check. The false branch exits the loop.

### Instructor notes

- Trace the condition before each iteration, including the final false check.
- Temporarily remove the update line and ask why the loop no longer stops.
- Keep `break` and `continue` as optional extensions, not core content.

### Notebook connection

The source notebook mainly uses collection operations, but understanding `while` completes the beginner model of repetition before later training loops.

### Sources

- [Python Tutorial: while Statements](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)
- [Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)

---

## Slide 10 - Functions Turn a Solution into Reusable Code

### Teaching purpose

Explain function definition, parameters, arguments, local work, and return values.

### Learner-facing content

A **function** is a named, reusable block of code.

```python
def average(values):
    total = sum(values)
    return total / len(values)
```

- `def` begins a function definition.
- `average` is the function name.
- `values` is a **parameter**, a name used inside the function.
- `[72, 85, 90]` is an **argument**, the actual value supplied when calling it.
- `return` sends a result back to the caller.

Defining a function does not run its body. The body runs when the function is called.

### Worked example

Call:

```python
average([72, 85, 90])
```

Inside the function:

1. `values` refers to `[72, 85, 90]`.
2. `sum(values)` gives `247`.
3. `len(values)` gives `3`.
4. `247 / 3` gives approximately `82.33`.
5. `return` sends that value back.

### Code example

```python
def average(values):
    total = sum(values)
    return total / len(values)


scores = [72, 85, 90]
mean_score = average(scores)

print(round(mean_score, 2))
```

Expected output:

```text
82.33
```

### Visual description

A function box receives the argument list, labels it as parameter `values`, performs two intermediate calculations, and returns `82.33`.

### Instructor notes

- Separate definition time from call time.
- Trace how the argument becomes the parameter value.
- Contrast `print()` with `return`: printing displays; returning supplies a reusable result.

### Notebook connection

This prepares learners to replace `pass` inside the notebook's `predict()` function and to understand its parameters.

### Sources

- [Python Tutorial: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Tutorial: return Statements](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)

---

## Slide 11 - Imports and Decomposition Manage Complexity

### Teaching purpose

Teach modules, imports, queues, and breaking a problem into smaller functions.

### Learner-facing content

A **module** is a Python file containing definitions and statements. An **import** makes code from a module available.

```python
from collections import deque
```

The standard-library `collections` module provides `deque`, a collection designed for adding and removing values from either end.

A **queue** processes items in first-in, first-out order.

As programs grow, use **problem decomposition**: split one large task into smaller tasks with clear inputs and outputs.

Example decomposition:

1. load scores;
2. calculate a summary;
3. assign a result; and
4. display the report.

### Worked example

Start with:

```python
tasks = deque(["load_data", "train_model", "evaluate_model"])
```

1. `popleft()` removes and returns `"load_data"`.
2. The remaining queue is `"train_model"`, then `"evaluate_model"`.
3. `append("save_model")` adds a task to the end.

The queue preserves the intended processing order.

### Code example

```python
from collections import deque

tasks = deque(["load_data", "train_model", "evaluate_model"])
current_task = tasks.popleft()

print(current_task)
print(tasks)
```

Expected output:

```text
load_data
deque(['train_model', 'evaluate_model'])
```

### Visual description

A queue enters from the right and exits from the left. Beneath it, one large program is decomposed into four small named steps.

### Instructor notes

- Explain that the standard library is installed with Python.
- Read the import statement from right to left: get `deque` from `collections`.
- Keep packages, installation, and custom modules for later practical work.

### Notebook connection

This directly prepares learners for the notebook's `deque` task queue. It also explains how to divide the incomplete prediction task into smaller steps.

### Sources

- [Python Tutorial: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python Documentation: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)

---

## Slide 12 - Worked Program: Summarize Quiz Scores

### Teaching purpose

Combine a list, loop, condition, function, and dictionary in one traceable program.

### Learner-facing content

Problem: Given several quiz scores, calculate:

- the number of scores;
- the average score; and
- how many scores are passes using a threshold of `70`.

Plan:

1. Store the scores in a list.
2. Define a function that receives the list.
3. Use a loop and condition to count passes.
4. Calculate the average.
5. Return the results in a dictionary.

Each structure has one job: the list stores repeated values, the loop visits them, the condition classifies them, and the dictionary names the results.

### Worked example

For `[72, 85, 90, 68]`:

1. Count: `4`
2. Total: `72 + 85 + 90 + 68 = 315`
3. Average: `315 / 4 = 78.75`
4. Passing scores: `72`, `85`, and `90`
5. Pass count: `3`

Returned summary:

```python
{"count": 4, "average": 78.75, "passes": 3}
```

### Code example

```python
def summarize(scores):
    passes = 0

    for score in scores:
        if score >= 70:
            passes = passes + 1

    return {
        "count": len(scores),
        "average": sum(scores) / len(scores),
        "passes": passes,
    }


quiz_scores = [72, 85, 90, 68]
summary = summarize(quiz_scores)

print(summary)
```

Expected output:

```text
{'count': 4, 'average': 78.75, 'passes': 3}
```

### Visual description

The list flows through a function. Inside, a loop visits each score, a condition marks pass or review, and three named outputs enter a dictionary.

### Instructor notes

- Ask learners to trace `passes` through all four iterations.
- Change the threshold to `80` and predict the new result before running.
- End with a notebook-readiness check: list updates, key lookup, set uniqueness, tuple unpacking, branches, loops, functions, and imports.

### Notebook connection

Learners are ready for the notebook's data-structure cells, `deque` example, and placeholder functions. The `lambda` and `map()` cells should be treated as optional instructor-led extensions after the ordinary loop and named-function versions are understood.

### Sources

- [Python Tutorial: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python Tutorial: Control Flow and Functions](https://docs.python.org/3/tutorial/controlflow.html)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Approval Gate

This Markdown is the review source for Week 2. Its wording, examples, and slide order may be revised during review.

No presentation, PDF, narration, video, or LMS asset should be created or replaced until this Markdown is explicitly approved.
