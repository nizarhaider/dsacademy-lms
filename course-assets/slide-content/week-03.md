# Week 3: Data Analysis with NumPy and Pandas

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who have completed Weeks 1 and 2  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 3 presentation and related media.

---

## Slide 1 - A Dataset Is a Collection of Observations

### Teaching purpose

Move from Python collections to the row-and-column model used in data science.

### Learner-facing content

A **dataset** is an organized collection of observations.

- A **row** represents one observation.
- A **column** represents one measured property.
- The **row grain** states exactly what one row represents.

Example: in a class-results dataset, one row could represent one student. Columns could contain the student's name, course, score, and attendance.

The row grain must remain consistent. If some rows represent students and others represent entire classes, calculations such as averages no longer have a clear meaning.

### Worked example

| student | course | score |
|---|---|---:|
| Asha | Python | 72 |
| Ben | Python | 84 |
| Chen | AI | 91 |

There are `3` observations and `3` variables. The row grain is **one student's result in one course**.

### Code example

```python
records = [
    {"student": "Asha", "course": "Python", "score": 72},
    {"student": "Ben", "course": "Python", "score": 84},
]
print(len(records))
```

Expected output:

```text
2
```

### Visual description

A small table with one row highlighted as an observation and one column highlighted as a variable. A label below states the row grain.

### Instructor notes

Ask what one row represents before discussing Pandas. Show how an unclear grain produces misleading totals.

### Notebook connection

The notebook creates arrays and DataFrames. Learners must identify observations and variables before using those objects.

### Sources

- [Pandas: DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Slide 2 - NumPy Arrays Store Shaped Numerical Data

### Teaching purpose

Define arrays, dimensions, shapes, sizes, and data types.

### Learner-facing content

A NumPy **array** is a collection of values arranged along one or more axes. Array values normally share one **data type**.

- `ndim`: number of axes
- `shape`: length of each axis
- `size`: total number of values
- `dtype`: type used to store the values

For a two-dimensional array, shape `(2, 3)` means `2` rows and `3` columns. Its size is `2 x 3 = 6`.

### Worked example

```text
[[72, 80, 75],
 [84, 79, 88]]
```

1. Axes: `2`
2. Shape: `(2, 3)`
3. Size: `6`
4. If all values are whole numbers, the data type is an integer type.

### Code example

```python
import numpy as np

scores = np.array([[72, 80, 75], [84, 79, 88]])
print(scores.ndim, scores.shape, scores.size)
```

Expected output:

```text
2 (2, 3) 6
```

### Visual description

A 2-by-3 number grid with braces marking axis 0 as rows and axis 1 as columns. The shape `(2, 3)` appears beside it.

### Instructor notes

Have learners count rows and columns before revealing the shape. Explain that shape errors are often more important than syntax errors in numerical code.

### Notebook connection

This prepares learners to inspect tensor and array shapes instead of treating them as unexplained output.

### Sources

- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy for Absolute Beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)

---

## Slide 3 - Indexing Selects Values from an Array

### Teaching purpose

Connect Week 2 indexing to one- and two-dimensional arrays.

### Learner-facing content

An **index** identifies a position. NumPy starts counting at zero.

For a two-dimensional array, use `[row, column]`:

```python
scores[1, 2]
```

This means row index `1` and column index `2`. A colon means “take all positions along this axis.”

- `scores[0, :]`: every column from the first row
- `scores[:, 1]`: every row from the second column
- `scores[0:2, 1:3]`: a rectangular slice

### Worked example

Using:

```text
[[72, 80, 75],
 [84, 79, 88]]
```

`scores[1, 2]` gives `88`.  
`scores[:, 1]` gives `[80, 79]`.

### Code example

```python
print(scores[1, 2])
print(scores[:, 1])
```

Expected output:

```text
88
[80 79]
```

### Visual description

The grid from Slide 2 appears with row and column indexes. One cell and then one complete column are highlighted.

### Instructor notes

Read every selection aloud as “row, column.” Ask learners to predict the shape of a selection before running it.

### Notebook connection

Notebook operations select feature columns and individual values using the same positional idea.

### Sources

- [NumPy: Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Slide 4 - Vectorized Operations Work on Whole Arrays

### Teaching purpose

Explain why NumPy operations differ from manual Python loops.

### Learner-facing content

A **vectorized operation** applies one operation to an entire array.

```python
scores + 5
```

adds `5` to every score. NumPy performs the repeated numerical work in optimized array code.

**Broadcasting** is NumPy's rule for combining arrays with compatible shapes. A single number can be expanded conceptually to match every element. Compatible dimensions are equal, or one of them is `1`.

Vectorization makes the intended calculation visible and reduces manual loop code.

### Worked example

Original: `[72, 84, 91]`  
Adjustment: `+ 5`  
Result: `[77, 89, 96]`

The same addition is applied to all three positions.

### Code example

```python
scores = np.array([72, 84, 91])
adjusted = scores + 5
print(adjusted)
```

Expected output:

```text
[77 89 96]
```

### Visual description

Three values flow through one `+ 5` operation into three adjusted values. A smaller warning shows incompatible shapes `(2, 3)` and `(2,)`.

### Instructor notes

Contrast this with a `for` loop from Week 2. Keep broadcasting to scalar and row-vector examples.

### Notebook connection

The notebook uses array arithmetic and aggregations that operate over complete collections.

### Sources

- [NumPy: Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)

---

## Slide 5 - Series and DataFrames Add Labels

### Teaching purpose

Define the two core Pandas objects and distinguish them from raw arrays.

### Learner-facing content

A Pandas **Series** is a one-dimensional labelled collection. A **DataFrame** is a two-dimensional labelled table.

Labels make data easier to interpret:

- row labels form the **index**;
- column labels identify variables;
- each column has a data type;
- different columns may use different types.

NumPy is strongest for shaped numerical arrays. Pandas is designed for labelled tabular data that may contain numbers, text, dates, booleans, and missing values.

### Worked example

The dictionary:

```python
{"student": ["Asha", "Ben"], "score": [72, 84]}
```

becomes a DataFrame with two rows and two named columns. Its shape is `(2, 2)`.

### Code example

```python
import pandas as pd

df = pd.DataFrame({
    "student": ["Asha", "Ben"],
    "score": [72, 84],
})
print(df.shape)
```

Expected output:

```text
(2, 2)
```

### Visual description

A NumPy grid receives row and column labels and becomes a DataFrame. Column type badges show text and integer.

### Instructor notes

Emphasize that a DataFrame is not a spreadsheet file; it is a Python object in memory.

### Notebook connection

Learners can now read DataFrame construction and understand why named columns are useful.

### Sources

- [Pandas: Intro to Data Structures](https://pandas.pydata.org/docs/user_guide/dsintro.html)
- [Pandas: DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

---

## Slide 6 - Load Data, Then Inspect Before Transforming

### Teaching purpose

Teach a safe first inspection sequence for CSV and JSON data.

### Learner-facing content

A **CSV** file stores table rows as comma-separated text. **JSON** represents nested objects, arrays, strings, numbers, booleans, and null values.

Loading creates a DataFrame:

```python
df = pd.read_csv("results.csv")
```

Before changing the data, inspect:

1. `df.shape` for row and column counts;
2. `df.head()` for example rows;
3. `df.columns` for variable names;
4. `df.dtypes` for stored types;
5. `df.isna().sum()` for missing values.

### Worked example

If `df.shape` is `(120, 4)`, the table has `120` rows and `4` columns. This does not prove that all rows are valid; it only states the current shape.

### Code example

```python
df = pd.read_csv("results.csv")
print(df.shape)
print(df.dtypes)
print(df.isna().sum())
```

Expected output:

```text
(120, 4)
student       object
course        object
score        float64
attendance     int64
```

### Visual description

A file icon flows into a DataFrame, followed by five inspection checkpoints.

### Instructor notes

Explain that `object` commonly stores text. Do not promise exact output for an unknown file; the example output describes one sample dataset.

### Notebook connection

This inspection routine should be used before every notebook transformation.

### Sources

- [Pandas: IO Tools](https://pandas.pydata.org/docs/user_guide/io.html)
- [Pandas: Essential Basic Functionality](https://pandas.pydata.org/docs/user_guide/basics.html)

---

## Slide 7 - Select, Filter, and Sort Rows Deliberately

### Teaching purpose

Explain labelled selection and boolean filtering.

### Learner-facing content

**Selection** chooses columns or rows. **Filtering** keeps rows that satisfy a condition. **Sorting** changes row order without changing the values.

```python
passed = df[df["score"] >= 50]
```

The comparison creates a **boolean mask**: one `True` or `False` value per row. Pandas keeps rows where the mask is `True`.

Use `.loc[rows, columns]` when selecting by labels:

```python
passed = df.loc[df["score"] >= 50, ["student", "score"]]
```

### Worked example

Scores `[42, 68, 91]` produce mask `[False, True, True]`. Filtering keeps `[68, 91]`. Sorting descending produces `[91, 68]`.

### Code example

```python
passed = (
    df.loc[df["score"] >= 50, ["student", "score"]]
      .sort_values("score", ascending=False)
)
print(passed)
```

Expected output:

```text
  student  score
2    Chen     91
1     Ben     68
```

### Visual description

Three table rows align with a three-value boolean mask; false rows fade while true rows move into the filtered table.

### Instructor notes

Trace the mask before showing the filtered result. Distinguish row selection from changing values.

### Notebook connection

The notebook uses masks to isolate relevant observations before analysis.

### Sources

- [Pandas: Indexing and Selecting Data](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas: DataFrame.sort_values](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html)

---

## Slide 8 - Missing Values Need an Explicit Policy

### Teaching purpose

Define missing values and introduce reasoned handling choices.

### Learner-facing content

A **missing value** records that an observation is absent or unknown. Pandas commonly displays it as `NaN` or `NA`.

Missing does not automatically mean zero. A missing score could mean:

- the student did not take the test;
- the score was not recorded;
- the file was parsed incorrectly; or
- the value was removed by a rule.

Possible actions are to retain, collect again, exclude, or **impute** a replacement. The correct choice depends on why the value is missing and how the result will be used.

### Worked example

Scores: `[72, missing, 84]`

- Filling with `0` gives mean `(72 + 0 + 84) / 3 = 52`.
- Ignoring the missing value gives mean `(72 + 84) / 2 = 78`.

The policy changes the conclusion.

### Code example

```python
print(df["score"].isna().sum())
print(df["score"].mean())
```

Expected output:

```text
1
78.0
```

### Visual description

One missing cell branches into retain, investigate, impute, and exclude paths. Each path includes a “document why” label.

### Instructor notes

Ask why the value is missing before discussing methods such as `fillna()` or `dropna()`.

### Notebook connection

Learners must inspect and explain missing-value handling before producing summaries.

### Sources

- [Pandas: Working with Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Pandas: DataFrame.isna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html)

---

## Slide 9 - Grouping Answers Questions About Categories

### Teaching purpose

Explain split-apply-combine with a fully worked aggregation.

### Learner-facing content

**Grouping** divides rows into categories. An **aggregation** reduces each group to a summary such as count, sum, mean, minimum, or maximum.

The GroupBy process is:

1. **Split** rows by a key such as `course`.
2. **Apply** a calculation such as mean score.
3. **Combine** one result for each group.

### Worked example

| course | score |
|---|---:|
| Python | 72 |
| Python | 84 |
| AI | 91 |

Python mean: `(72 + 84) / 2 = 78`  
AI mean: `91 / 1 = 91`

### Code example

```python
means = df.groupby("course")["score"].mean()
print(means)
```

Expected output:

```text
course
AI        91.0
Python    78.0
```

### Visual description

Rows split into two coloured course groups, each passes through a mean calculation, and two results are recombined.

### Instructor notes

Calculate both means by hand. Point out that group size should be reported because a mean from one row is less stable than a mean from many rows.

### Notebook connection

The notebook uses grouping to turn detailed rows into interpretable summaries.

### Sources

- [Pandas: GroupBy, Split-Apply-Combine](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas GroupBy Reference](https://pandas.pydata.org/docs/reference/groupby.html)

---

## Slide 10 - A Complete Table Analysis Has Visible Steps

### Teaching purpose

Combine loading, inspection, filtering, and grouping into one readable workflow.

### Learner-facing content

A reliable analysis should make each transformation inspectable:

1. load the source;
2. inspect shape, columns, types, and missingness;
3. state the row filter;
4. group at the intended level;
5. calculate a named summary;
6. verify at least one result by hand.

Method chains are useful only when learners can explain what each method receives and returns.

### Worked example

Question: “What is the average valid score per course?”

- Valid means score is present and between `0` and `100`.
- Group key is `course`.
- Summary is mean score plus number of rows.

### Code example

```python
valid = df[df["score"].between(0, 100)]
summary = valid.groupby("course").agg(
    students=("student", "count"),
    mean_score=("score", "mean"),
)
print(summary)
```

Expected output:

```text
        students  mean_score
course
AI             1        91.0
Python         2        78.0
```

### Visual description

A six-stage pipeline with a small table snapshot after the filter and after the aggregation.

### Instructor notes

Ask learners to label every line as input, selection, grouping, or aggregation.

### Notebook connection

This is the reasoning pattern learners should apply to the Pandas section of the notebook.

### Sources

- [Pandas: Getting Started Tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)

---

## Slide 11 - Common Mistakes Change the Meaning

### Teaching purpose

Make semantic errors visible before the guided lab.

### Learner-facing content

Common mistakes:

- reading shape `(3, 4)` as four rows and three columns;
- confusing a column label with a row position;
- filtering with a mask of the wrong length;
- calculating along the wrong axis;
- treating missing values as zero without justification;
- grouping before checking the row grain;
- reporting a mean without reporting the group count.

Data code can run successfully and still answer the wrong question. Verification requires checking shapes, sample rows, counts, and one result by hand.

### Worked example

For a `(2, 3)` array, `scores.mean(axis=0)` produces one mean for each of `3` columns. `scores.mean(axis=1)` produces one mean for each of `2` rows.

### Code example

```python
print(scores.mean(axis=0).shape)
print(scores.mean(axis=1).shape)
```

Expected output:

```text
(3,)
(2,)
```

### Visual description

Two arrows traverse the same matrix: axis 0 moves down rows and axis 1 moves across columns, producing outputs of different lengths.

### Instructor notes

Use prediction before execution. The goal is to reason from shapes rather than memorize axis numbers.

### Notebook connection

The notebook-readiness check is to predict output shapes and row counts before running each operation.

### Sources

- [NumPy Quickstart: Axis Operations](https://numpy.org/doc/stable/user/quickstart.html)
- [Pandas: Indexing and Selecting Data](https://pandas.pydata.org/docs/user_guide/indexing.html)

---

## Slide 12 - Guided Lab: Explain a Small Dataset

### Teaching purpose

Define the Week 3 practical task and readiness standard.

### Learner-facing content

Use a small CSV containing students, courses, scores, and attendance.

Complete these steps:

1. State what one row represents.
2. Report shape, columns, and data types.
3. Count missing values.
4. Keep scores from `0` to `100`.
5. Calculate count and mean score per course.
6. Verify one group mean by hand.
7. Explain one limitation of the dataset.

You are ready for Week 4 when you can explain every row-selection and aggregation step without relying only on the final output.

### Worked example

For Python scores `72` and `84`, the independent check is:

`(72 + 84) / 2 = 78`

The DataFrame result should also be `78.0`.

### Code example

```python
assert valid["score"].between(0, 100).all()
print(summary)
```

Expected output:

```text
The assertion passes, followed by one summary row per course.
```

### Visual description

A checklist connects “row grain” to “inspect,” “filter,” “group,” “verify,” and “explain.”

### Instructor notes

Require predictions before execution and short explanations after each output. Do not accept a notebook containing only code and final tables.

### Notebook connection

Continue into the NumPy and Pandas sections of `01.python-essentials-for-ai.ipynb`.

### Sources

- [AI Bootcamp: Python Essentials for AI](https://github.com/curiousily/AI-Bootcamp/blob/master/01.python-essentials-for-ai.ipynb)
- [Pandas: Getting Started](https://pandas.pydata.org/docs/getting_started/)
