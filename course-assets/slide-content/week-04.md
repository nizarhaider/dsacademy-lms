# Week 4: Exploratory Data Analysis

**Status:** PRODUCTION AUTHORIZED

**Audience:** Beginners who can inspect and summarize a DataFrame  
**Language:** English  
**Production rule:** This Markdown is the sole teaching-content source for the Week 4 presentation and related media.

---

## Slide 1 - EDA Asks What the Data Can Support

### Teaching purpose

Define exploratory data analysis as a question-driven process before modelling.

### Learner-facing content

**Exploratory data analysis (EDA)** is the process of examining a dataset to understand its structure, quality, distributions, and relationships.

EDA helps answer:

- What does one row represent?
- Which values are missing, invalid, or unusual?
- What values are typical?
- How spread out are the values?
- Which groups differ?
- Which relationships deserve further investigation?

EDA produces evidence and new questions. It does not automatically prove why a pattern exists.

### Worked example

Question: “Do customers who subscribed differ in age from those who did not?”

Before comparing ages, check the row grain, missing values, valid age range, and the number of customers in each group.

### Code example

```python
print(df.shape)
print(df["subscribed"].value_counts(dropna=False))
```

Expected output:

```text
One row count and the number of records in each target class.
```

### Visual description

A question sits at the center of a loop: structure, quality, distribution, relationship, interpretation.

### Instructor notes

Require a question before a chart. Explain that “plot every column” is not a useful analytical objective.

### Notebook connection

The EDA notebook begins with data loading and an initial assessment before feature work.

### Sources

- [AI Bootcamp: Exploratory Data Analysis](https://github.com/curiousily/AI-Bootcamp/blob/master/02.exploratory-data-analysis.ipynb)
- [NIST: Exploratory Data Analysis](https://www.itl.nist.gov/div898/handbook/eda/eda.htm)

---

## Slide 2 - Start with Schema, Grain, and Quality Rules

### Teaching purpose

Teach learners to establish what the table means before calculating statistics.

### Learner-facing content

A **schema** describes column names, data types, and expected meanings. A **quality rule** states what a valid value or row must satisfy.

Examples:

- age must be between `18` and `100`;
- customer ID must be unique;
- balance may be negative, so “negative” is not automatically invalid;
- `"unknown"` may be a missing-value marker rather than a real category.

Data types describe storage. They do not guarantee meaning. A numeric age column can still contain impossible values.

### Worked example

If a table has `4,521` rows but only `4,510` unique customer IDs, at least `11` rows repeat an ID. The duplicates must be investigated before treating rows as independent customers.

### Code example

```python
print(df.dtypes)
print(df["customer_id"].nunique())
print(df["age"].between(18, 100).all())
```

Expected output:

```text
Column types, a unique-ID count, and True or False for the age rule.
```

### Visual description

A schema panel sits beside three rule checks: uniqueness, valid range, and declared missing markers.

### Instructor notes

Ask whether a value is impossible, unusual, or merely unexpected. These require different responses.

### Notebook connection

This prepares learners for the notebook's initial assessment and data-quality checks.

### Sources

- [Pandas: DataFrame.dtypes](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html)
- [Pandas: DataFrame.nunique](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nunique.html)

---

## Slide 3 - Center Describes a Typical Value

### Teaching purpose

Explain mean and median with a skewed numerical example.

### Learner-facing content

The **mean** is the sum divided by the number of values:

`mean = (x1 + x2 + ... + xn) / n`

The **median** is the middle value after sorting.

The mean uses every value and is pulled toward extremes. The median depends on order and is more resistant to extreme values. Neither is always “better”; choose the statistic that answers the question and describe the distribution.

### Worked example

Values: `[20, 22, 24, 26, 200]`

Mean:

`(20 + 22 + 24 + 26 + 200) / 5 = 292 / 5 = 58.4`

Median: the ordered middle value is `24`.

The value `200` pulls the mean far above most observations.

### Code example

```python
values = pd.Series([20, 22, 24, 26, 200])
print(values.mean(), values.median())
```

Expected output:

```text
58.4 24.0
```

### Visual description

A number line shows four values clustered near 20–26 and one at 200. Mean and median markers appear at different locations.

### Instructor notes

Calculate both statistics by hand. Avoid describing the median as an average without naming which average.

### Notebook connection

Learners will compare descriptive statistics and explain why one summary can hide skew.

### Sources

- [NIST: Measures of Location](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm)
- [Pandas: Series.describe](https://pandas.pydata.org/docs/reference/api/pandas.Series.describe.html)

---

## Slide 4 - Spread Describes How Values Vary

### Teaching purpose

Define range, variance, standard deviation, and interquartile range.

### Learner-facing content

**Spread** describes how far values vary.

- **Range:** maximum minus minimum
- **Variance:** average squared distance from the mean
- **Standard deviation:** square root of variance
- **Interquartile range (IQR):** third quartile minus first quartile

Standard deviation uses every value and has the same units as the data. IQR describes the middle half of ordered values and is less affected by extremes.

### Worked example

For `[2, 4, 6]`, mean is `4`.

Squared distances: `(2-4)^2 = 4`, `(4-4)^2 = 0`, `(6-4)^2 = 4`

Population variance: `(4 + 0 + 4) / 3 = 2.67`  
Population standard deviation: `sqrt(2.67) ≈ 1.63`

### Code example

```python
values = pd.Series([2, 4, 6])
print(values.var(ddof=0))
print(values.std(ddof=0))
```

Expected output:

```text
2.6666666666666665
1.632993161855452
```

### Visual description

Three points on a number line have arrows to the mean. A second strip labels Q1, median, Q3, and IQR.

### Instructor notes

State whether population or sample variance is used. The worked example uses division by `n` through `ddof=0`.

### Notebook connection

Spread helps learners compare variables and detect distributions that need closer inspection.

### Sources

- [NIST: Measures of Scale](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm)
- [Pandas: Series.var](https://pandas.pydata.org/docs/reference/api/pandas.Series.var.html)

---

## Slide 5 - A Distribution Shows Frequency and Shape

### Teaching purpose

Teach learners to read histograms as counts across value intervals.

### Learner-facing content

A **distribution** describes which values occur and how often.

A **histogram** divides a numerical range into intervals called bins. Bar height shows how many observations fall inside each interval.

Common shapes include:

- roughly symmetric;
- right-skewed with a long high-value tail;
- left-skewed with a long low-value tail;
- multimodal with more than one peak.

Changing bin width can reveal or hide structure, so inspect more than one reasonable setting.

### Worked example

Scores `[42, 48, 51, 55, 56, 82, 88]` have a cluster around 42–56 and a smaller cluster around 82–88. The mean alone would not show both groups.

### Code example

```python
df["score"].plot.hist(bins=5)
```

Expected output:

```text
A histogram with score intervals on the x-axis and counts on the y-axis.
```

### Visual description

Three miniature histograms show symmetric, right-skewed, and two-peaked shapes with axes labelled.

### Instructor notes

Ask what each axis means. Do not call a histogram a bar chart: histogram bars represent continuous intervals.

### Notebook connection

The notebook's visualizations should be interpreted in words, not included as decoration.

### Sources

- [NIST: Histogram](https://www.itl.nist.gov/div898/handbook/eda/section3/histogra.htm)
- [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)

---

## Slide 6 - Outliers Are Signals to Investigate

### Teaching purpose

Define outliers and explain the IQR flag without treating it as an automatic deletion rule.

### Learner-facing content

An **outlier** is an observation unusually far from most values under a stated rule.

One common flag uses the IQR:

- lower fence: `Q1 - 1.5 x IQR`
- upper fence: `Q3 + 1.5 x IQR`

A value beyond a fence is a candidate for investigation. It may be a data error, a rare valid case, or evidence of a separate group. Removing it without checking can erase important information.

### Worked example

If `Q1 = 20` and `Q3 = 40`:

`IQR = 40 - 20 = 20`  
Lower fence: `20 - 1.5 x 20 = -10`  
Upper fence: `40 + 1.5 x 20 = 70`

A value of `95` is flagged because `95 > 70`.

### Code example

```python
q1 = df["value"].quantile(0.25)
q3 = df["value"].quantile(0.75)
iqr = q3 - q1
outliers = df[~df["value"].between(q1 - 1.5*iqr, q3 + 1.5*iqr)]
```

Expected output:

```text
A DataFrame containing values outside the stated fences.
```

### Visual description

A box plot labels Q1, median, Q3, whiskers, and one flagged point. Three investigation paths appear beside it.

### Instructor notes

Use the phrase “flagged by this rule,” not “wrong.” Ask what source evidence would justify correction.

### Notebook connection

Learners should record how unusual values are detected and what decision follows.

### Sources

- [NIST: Box Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm)
- [Pandas: DataFrame.quantile](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.quantile.html)

---

## Slide 7 - Missing Markers and Categories Need Counting

### Teaching purpose

Show how hidden missing values and rare categories affect analysis.

### Learner-facing content

Missing information may appear as `NaN`, an empty string, `-1`, `"unknown"`, or `"not applicable"`. These are **sentinel values** when they stand in for another meaning.

For categorical columns:

- count each category;
- include missing values;
- inspect spelling and capitalization;
- confirm whether sentinel values are real categories;
- report both counts and percentages.

A rare category may be valid and important. Combining categories requires a stated reason.

### Worked example

Job values:

```text
teacher, teacher, unknown, Teacher, missing
```

Without cleaning, `teacher` and `Teacher` are counted separately. `"unknown"` and missing may represent two different data-collection outcomes.

### Code example

```python
print(df["job"].value_counts(dropna=False))
```

Expected output:

```text
One count for every observed category, including missing values.
```

### Visual description

A raw category list flows into a frequency table. Potential spelling variants and sentinel markers are highlighted, not silently merged.

### Instructor notes

Ask learners to distinguish normalization of spelling from changing meaning.

### Notebook connection

This prepares the notebook's quality checks and categorical visualizations.

### Sources

- [Pandas: Series.value_counts](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
- [Pandas: Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)

---

## Slide 8 - Class Imbalance Changes How Accuracy Feels

### Teaching purpose

Introduce target balance before formal classification metrics in Week 8.

### Learner-facing content

A **target** is the outcome a supervised model will learn to predict. For a categorical target, each possible value is a **class**.

**Class imbalance** occurs when one class is much more common than another.

If `90` of `100` customers did not subscribe, a rule that always predicts “no” is `90%` accurate. It still identifies none of the `10` subscribers.

This is why EDA must count target classes before modelling. The appropriate evaluation measure depends on which mistakes matter.

### Worked example

Actual counts:

- No: `90`
- Yes: `10`

Always predict No:

`accuracy = 90 correct / 100 total = 0.90`

Subscribers found: `0 / 10 = 0`.

### Code example

```python
counts = df["subscribed"].value_counts()
percent = df["subscribed"].value_counts(normalize=True)
print(counts, percent)
```

Expected output:

```text
Counts and proportions for each class.
```

### Visual description

A 100-cell grid contains 90 neutral cells and 10 accent cells. A large “90% accuracy” label is paired with “0 subscribers found.”

### Instructor notes

Do not teach precision and recall formulas yet. Use this example to motivate why accuracy alone can mislead.

### Notebook connection

The notebook's target distribution should be described before feature importance or modelling.

### Sources

- [Scikit-learn: Classification Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [AI Bootcamp: Exploratory Data Analysis](https://github.com/curiousily/AI-Bootcamp/blob/master/02.exploratory-data-analysis.ipynb)

---

## Slide 9 - Relationships Do Not Automatically Mean Causation

### Teaching purpose

Define association, correlation, and causation.

### Learner-facing content

An **association** means two variables vary together in the observed data.

**Correlation** summarizes the direction and strength of a linear relationship between two numerical variables. Pearson correlation ranges from `-1` to `1`.

- near `1`: strong positive linear relationship;
- near `-1`: strong negative linear relationship;
- near `0`: weak linear relationship.

**Causation** means changing one factor produces a change in another. Correlation alone does not establish causation because confounding factors, selection, timing, or chance may explain the pattern.

### Worked example

Suppose study hours and scores have correlation `0.70`. This supports a positive association in this dataset. It does not prove that adding one study hour causes a fixed score increase.

### Code example

```python
print(df[["study_hours", "score"]].corr())
```

Expected output:

```text
A 2-by-2 correlation matrix with 1.0 on the diagonal.
```

### Visual description

A scatter plot slopes upward. A separate causal arrow is crossed out and labelled “requires stronger evidence.”

### Instructor notes

Ask for possible confounders such as prior knowledge, course difficulty, or access to tutoring.

### Notebook connection

Learners should use cautious language when interpreting correlations and feature importance.

### Sources

- [NIST: Scatter Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/scatterp.htm)
- [Pandas: DataFrame.corr](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)

---

## Slide 10 - Feature Engineering Creates Measurable Inputs

### Teaching purpose

Explain feature engineering as a documented transformation, not arbitrary column creation.

### Learner-facing content

A **feature** is an input variable available when a prediction must be made. **Feature engineering** creates a feature from existing data using a stated rule.

Examples:

- `contact_duration_minutes = seconds / 60`
- `has_previous_contact = previous_contacts > 0`
- extract month from a valid contact date

A useful feature has:

- a clear meaning;
- a reproducible formula;
- valid source columns;
- no future information;
- checks for missing or impossible results.

### Worked example

If contact duration is `150` seconds:

`150 / 60 = 2.5` minutes

If duration is missing, the engineered value is also missing unless a documented policy says otherwise.

### Code example

```python
df["duration_minutes"] = df["duration_seconds"] / 60
print(df[["duration_seconds", "duration_minutes"]].head())
```

Expected output:

```text
Each valid seconds value paired with its value divided by 60.
```

### Visual description

Two source columns flow through labelled formulas into two engineered feature columns. A red boundary marks unavailable future information.

### Instructor notes

Ask whether each source value would exist at prediction time. This previews leakage in Week 6.

### Notebook connection

The notebook creates features after initial assessment; learners must explain each transformation.

### Sources

- [Scikit-learn: Common Pitfalls and Leakage](https://scikit-learn.org/stable/common_pitfalls.html)
- [AI Bootcamp: Exploratory Data Analysis](https://github.com/curiousily/AI-Bootcamp/blob/master/02.exploratory-data-analysis.ipynb)

---

## Slide 11 - A Reproducible EDA Has a Question and Evidence

### Teaching purpose

Combine EDA steps into a repeatable analytical workflow.

### Learner-facing content

For each EDA question:

1. state the question;
2. identify required columns and row grain;
3. check missing, invalid, and duplicate values;
4. calculate a relevant statistic;
5. create a chart that answers the question;
6. interpret the pattern in plain language;
7. record limitations and the next question.

Every chart needs a title, labelled axes, units, and a written interpretation. Every transformation needs an inspectable output.

### Worked example

Question: “How does account balance differ by subscription outcome?”

Evidence:

- group counts;
- median and IQR of balance per class;
- side-by-side box plots;
- note that the comparison is observational and may be affected by other variables.

### Code example

```python
summary = df.groupby("subscribed")["balance"].agg(
    count="count", median="median"
)
print(summary)
```

Expected output:

```text
One row per class with its non-missing count and median balance.
```

### Visual description

A seven-step EDA loop ends in an evidence panel containing a statistic, chart, interpretation, and limitation.

### Instructor notes

Reject interpretations that merely repeat axis labels. Ask what the pattern means and what it does not prove.

### Notebook connection

This workflow maps directly to the notebook's assessment, statistics, visualization, and feature sections.

### Sources

- [NIST: EDA Approach](https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm)
- [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)

---

## Slide 12 - Guided Lab: Produce Three Defensible Findings

### Teaching purpose

Set the Week 4 deliverable and readiness criteria for machine learning.

### Learner-facing content

Use the Bank Marketing dataset to produce three findings.

Your report must include:

1. row grain and target definition;
2. shape, types, missing markers, and duplicate checks;
3. target class counts and percentages;
4. one numerical distribution with center and spread;
5. one group comparison;
6. one relationship between numerical variables;
7. one documented feature idea;
8. limitations and an unanswered question.

Do not make causal claims from correlation or feature importance.

### Worked example

Finding format:

“The median balance was higher in group A than group B. Group sizes were `nA` and `nB`. This is an observed association; the data does not establish that balance caused the outcome.”

### Code example

```python
assert len(df) > 0
assert df["subscribed"].notna().all()
```

Expected output:

```text
Both assertions pass before target analysis begins.
```

### Visual description

A report page contains three evidence rows: question, statistic or chart, interpretation, and limitation.

### Instructor notes

Require learners to verify at least one statistic by hand and explain why each chart was chosen.

### Notebook connection

Continue into `02.exploratory-data-analysis.ipynb`, treating notebook cells as the lab rather than the lesson outline.

### Sources

- [AI Bootcamp: Exploratory Data Analysis](https://github.com/curiousily/AI-Bootcamp/blob/master/02.exploratory-data-analysis.ipynb)
- [UCI Bank Marketing Dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing)
