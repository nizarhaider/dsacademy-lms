# Week 1: Computational Thinking and Python Basics

**Status:** APPROVED - PRODUCTION AUTHORIZED

**Audience:** Complete beginners with no coding experience  
**Language:** English  
**Production rule:** This approved Markdown is the sole teaching-content source for the Week 1 presentation. PPTX production is authorized; narration, video, and LMS replacement remain out of scope for this review.

---

## Slide 1 - A Program Transforms Input into Output

### Teaching purpose

Introduce programming as a way to transform information by following instructions.

### Learner-facing content

A **program** is a set of instructions that a computer can execute.

Most programs can be understood using four parts:

- **Input:** information given to the program
- **Instructions:** the rules the program follows
- **Processing:** the work performed using those rules
- **Output:** the result produced by the program

Example: a program receives a rectangle's length of `5` and width of `3`. It multiplies them and displays an area of `15` square units.

The computer does not understand weather in the way a person does. It only follows the instructions written in the program.

### Worked example

Calculate the area of a rectangle:

1. Inputs: length `5` and width `3`
2. Instruction: multiply length by width
3. Processing: `5 x 3 = 15`
4. Output: `15` square units

### Code example

```python
length = 5
width = 3
area = length * width
print(area)
```

Expected output:

```text
15
```

### Visual description

A left-to-right flow with four labelled boxes:

`length 5 and width 3` -> `multiply` -> `5 x 3` -> `area 15`

### Instructor notes

- Ask learners to identify the input and output before showing the code.
- Emphasize that a program needs precise instructions, even for a familiar calculation.
- Do not explain variables or operators yet; those concepts appear later.

### Notebook connection

The source notebook later combines values and operations inside functions. This lesson first establishes those simpler building blocks.

### Sources

- [Python Tutorial: An Informal Introduction](https://docs.python.org/3/tutorial/introduction.html)
- [Software Carpentry: Python Fundamentals](https://swcarpentry.github.io/python-novice-inflammation/01-intro.html)

---

## Slide 2 - An Algorithm Is a Sequence of Steps

### Teaching purpose

Show learners how to plan a solution before writing Python.

### Learner-facing content

An **algorithm** is a finite, ordered sequence of steps for solving a problem.

The order matters. If we add `32` before multiplying, we calculate a different answer.

For rectangle area, the algorithm is:

1. Read the rectangle's length.
2. Read the rectangle's width.
3. Multiply the length by the width.
4. Display the area.

An algorithm is not tied to Python. It can be written in plain English first and translated into code afterward.

### Worked example

Correct order:

1. Read length: `5`
2. Read width: `3`
3. Calculate area: `5 x 3 = 15`
4. Display: `15 square units`

If the program tries to calculate the area before reading the dimensions, the required values do not yet exist. Instructions must appear in a usable order.

### Code example

```python
length = 5
width = 3
area = length * width
print(area)
```

Expected output:

```text
15
```

### Visual description

A numbered flowchart shows the four algorithm steps. A crossed-out alternate path tries to calculate before the dimensions are available.

### Instructor notes

- Ask learners to describe a familiar algorithm, such as making tea or logging into a website.
- Check that every proposed step is precise and ordered.
- Explain that planning an algorithm reduces guessing when coding.

### Notebook connection

Learners will use this same plan-first approach when reading functions and data-processing steps in the notebook.

### Sources

- [BBC Bitesize: What Is an Algorithm?](https://www.bbc.co.uk/bitesize/guides/z3bq7ty/revision/1)
- [Python Tutorial: An Informal Introduction](https://docs.python.org/3/tutorial/introduction.html)

---

## Slide 3 - Python Executes Statements in Order

### Teaching purpose

Explain how Python runs a simple program and how program state changes line by line.

### Learner-facing content

A **statement** is an instruction written in code.

Python normally executes statements from top to bottom, one line at a time. After each line, it remembers the values that have been created. The collection of values currently remembered by the program is its **state**.

Tracing means following the program line by line and recording how its state changes.

Python must calculate the right-hand side of an assignment before storing the result on the left-hand side.

### Worked example

Trace this program:

1. `length = 5`  
   State: `length` contains `5`
2. `width = 3`  
   State: `length` contains `5`; `width` contains `3`
3. `area = length * width`  
   Calculation: `5 x 3 = 15`  
   State: `area` contains `15`
4. `print(area)` displays `15`

### Code example

```python
length = 5
width = 3
area = length * width
print(area)
```

Expected output:

```text
15
```

### Visual description

A trace table with columns for line number, statement, `length`, `width`, `area`, and output. Empty cells are filled as each line executes.

### Instructor notes

- Reveal one trace-table row at a time.
- Distinguish values stored in memory from text displayed as output.
- Ask what would happen if the `width` line were removed.

### Notebook connection

Notebook cells also execute instructions and preserve values. Learners must understand execution order before running cells out of sequence.

### Sources

- [Python Tutorial: First Steps Towards Programming](https://docs.python.org/3/tutorial/introduction.html#first-steps-towards-programming)
- [Software Carpentry: Running and Quitting](https://swcarpentry.github.io/python-novice-inflammation/01-intro.html)

---

## Slide 4 - Values Have Types

### Teaching purpose

Introduce the four basic Python types needed in Week 1.

### Learner-facing content

A **value** is a piece of information used by a program. Every value has a **type**, which tells Python what kind of information it is and what operations are valid.

- **Integer (`int`):** a whole number, such as `25`
- **Float (`float`):** a number with a decimal point, such as `25.0`
- **String (`str`):** text inside quotation marks, such as `"Colombo"`
- **Boolean (`bool`):** either `True` or `False`

Quotation marks matter. `25` is a number, while `"25"` is text. Python can perform arithmetic with the number, but the text must first be converted.

### Worked example

Consider these four values:

| Value | Type | Meaning |
|---|---|---|
| `5` | `int` | a whole-number length |
| `3.5` | `float` | a width with decimal precision |
| `"Rectangle"` | `str` | a shape name |
| `True` | `bool` | a yes/no result |

Python's `type()` function can identify each type.

### Code example

```python
print(type(5))
print(type(3.5))
print(type("Rectangle"))
print(type(True))
```

Expected output:

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

### Visual description

Four labelled containers hold a whole number, decimal number, text value, and true/false value. Each container uses a distinct shape and label rather than relying only on color.

### Instructor notes

- Demonstrate that `"25"` includes quotation marks because it is text.
- Explain that `True` and `False` begin with capital letters in Python.
- Keep the definition practical; detailed computer representation is unnecessary here.

### Notebook connection

The notebook uses numeric, text, and boolean values inside larger data structures. Learners first need to recognize individual values.

### Sources

- [Python Standard Types](https://docs.python.org/3/library/stdtypes.html)
- [Python Tutorial: Numbers and Text](https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator)

---

## Slide 5 - Variables Store Values

### Teaching purpose

Explain variables, assignment, naming, and reassignment.

### Learner-facing content

A **variable** is a name that refers to a value.

```python
length = 5
```

The assignment operator `=` tells Python to:

1. Calculate the expression on the right.
2. Store its value using the name on the left.

In programming, `=` means "assign this value." It does not mean that two sides are permanently equal as in mathematics.

A variable can be **reassigned**, meaning the same name can later refer to a new value. Clear names such as `rectangle_length` make code easier to understand than vague names such as `x`.

### Worked example

```python
length = 5
length = 7
```

After line 1, `length` refers to `5`.  
After line 2, it refers to `7`.

The old value has been replaced for that variable.

`=` assigns a value. The comparison operator `==`, introduced later, asks whether two values are equal.

### Code example

```python
length = 5
print(length)

length = 7
print(length)
```

Expected output:

```text
5
7
```

### Visual description

A variable label `length` points first to a box containing `5`, then to a box containing `7`. An arrow shows the change after reassignment.

### Instructor notes

- Read the statement aloud as "length gets 5."
- Ask learners for meaningful names for a shape, its dimensions, and its area.
- Mention that names cannot contain spaces; use underscores between words.

### Notebook connection

Notebook code assigns data, calculation results, and models to variables. Meaningful variable names help learners follow those steps.

### Sources

- [Python Tutorial: An Informal Introduction](https://docs.python.org/3/tutorial/introduction.html)
- [Python Language Reference: Assignment Statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)

---

## Slide 6 - Expressions Calculate New Values

### Teaching purpose

Teach arithmetic operators and operation precedence through a simple area calculation.

### Learner-facing content

An **expression** combines values, variables, and operators to produce a new value.

Common arithmetic operators are:

| Operator | Meaning | Example |
|---|---|---|
| `+` | addition | `5 + 2` gives `7` |
| `-` | subtraction | `5 - 2` gives `3` |
| `*` | multiplication | `5 * 2` gives `10` |
| `/` | division | `5 / 2` gives `2.5` |
| `//` | whole-number division | `5 // 2` gives `2` |
| `%` | remainder | `5 % 2` gives `1` |

Python follows **precedence rules**: multiplication and division happen before addition and subtraction. Parentheses can make the intended order explicit.

### Worked example

For `length = 5` and `width = 3`:

```text
length * width
5 * 3
15
```

The expression produces a new integer value, `15`.

For a larger expression, parentheses clarify the order:

```text
(length + 2) * width
(5 + 2) * 3
7 * 3
21
```

### Code example

```python
length = 5
width = 3
area = length * width
print(area)
```

Expected output:

```text
15
```

### Visual description

An expression tree shows that the addition inside `(length + 2)` happens before multiplication. A second small example shows `135 // 60 = 2` and `135 % 60 = 15`.

### Instructor notes

- Calculate each intermediate result with the class.
- Use parentheses to make the formula readable, even where precedence already gives the same result.
- Preview `//` and `%` because they will be used in the final minutes converter.

### Notebook connection

Numeric expressions are required throughout the notebook and in later NumPy calculations.

### Sources

- [Python Reference: Operator Precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
- [Python Tutorial: Using Python as a Calculator](https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator)

---

## Slide 7 - Comparisons Produce Boolean Results

### Teaching purpose

Connect comparisons to `True` and `False` before conditions are introduced in Week 2.

### Learner-facing content

A **comparison** asks a question about two values. Its result is always a boolean: `True` or `False`.

| Operator | Question |
|---|---|
| `==` | Are the values equal? |
| `!=` | Are the values different? |
| `>` | Is the left value greater? |
| `<` | Is the left value smaller? |
| `>=` | Is the left value greater than or equal? |
| `<=` | Is the left value smaller than or equal? |

Remember:

- `=` assigns a value.
- `==` compares two values.

Comparisons allow programs to represent decisions. Week 2 will use these boolean results in `if` statements.

### Worked example

For `area = 15`:

1. `area > 20` asks whether `15` is greater than `20`.
2. The answer is `False`.
3. `area == 15` asks whether the value equals `15`.
4. The answer is `True`.

### Code example

```python
area = 15

print(area > 20)
print(area == 15)
print(area != 10)
```

Expected output:

```text
False
True
True
```

### Visual description

A number line marks `10`, `15`, and `20`. Three comparison questions point to clearly labelled `True` or `False` results.

### Instructor notes

- Ask learners to predict each result before running the code.
- Reinforce that a comparison creates a value; it does not yet choose which code runs.
- Avoid introducing compound boolean logic until Week 2.

### Notebook connection

The source notebook uses boolean expressions in filtering and validation. Week 2 will connect comparisons to program control.

### Sources

- [Python Standard Types: Comparisons](https://docs.python.org/3/library/stdtypes.html#comparisons)
- [Python Reference: Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)

---

## Slide 8 - Strings and Functions Create Readable Output

### Teaching purpose

Teach text values, function calls, and formatted output.

### Learner-facing content

A **string** is a sequence of text characters written inside quotation marks.

```python
shape = "Rectangle"
```

A **function** is reusable code that performs a task. We **call** a function by writing its name followed by parentheses.

`print()` is a built-in function that displays output.

An **f-string** combines text with values. Put the letter `f` before the opening quotation mark and place variables or expressions inside braces:

```python
print(f"{shape}: area = {area}")
```

The braces are replaced with their current values when the line runs.

### Worked example

Given:

```python
shape = "Rectangle"
length = 5
width = 3
area = 15
```

The f-string:

```python
f"{shape}: {length} x {width} = {area} square units"
```

becomes:

```text
Rectangle: 5 x 3 = 15 square units
```

### Code example

```python
shape = "Rectangle"
length = 5
width = 3
area = length * width

print(f"{shape}: {length} x {width} = {area} square units")
```

Expected output:

```text
Rectangle: 5 x 3 = 15 square units
```

### Visual description

An f-string template is shown above the final sentence. Arrows connect `{shape}`, `{length}`, `{width}`, and `{area}` to the values inserted into the output.

### Instructor notes

- Identify the function name, parentheses, and argument in `print(...)`.
- Explain that quotation marks define the string but are not displayed.
- Keep functions at the call level; function definitions belong in Week 2.

### Notebook connection

Learners will use `print()` to inspect values and f-strings to present results while working through notebook exercises.

### Sources

- [Python Built-in Function: print](https://docs.python.org/3/library/functions.html#print)
- [Python Tutorial: Formatted String Literals](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)

---

## Slide 9 - User Input Arrives as Text

### Teaching purpose

Show how programs receive keyboard input and why numeric conversion is necessary.

### Learner-facing content

The built-in `input()` function pauses the program, displays a prompt, and waits for the user to type.

The value returned by `input()` is always a string, even when the user types digits.

```python
length_text = input("Length: ")
```

If the user types `5`, the variable contains the string `"5"`, not the number `5`.

**Type conversion** changes a value from one type to another:

- `int("5")` produces the integer `5`.
- `float("5.5")` produces the float `5.5`.

Use `float()` for dimensions because a measurement may contain a decimal.

### Worked example

Suppose the user enters length `5` and width `3`:

1. `input()` returns `"5"` and `"3"` as strings.
2. `float()` converts them to `5.0` and `3.0`.
3. Multiplication calculates `5.0 x 3.0`.
4. The area is `15.0`.

### Code example

```python
length_text = input("Length: ")
width_text = input("Width: ")

length = float(length_text)
width = float(width_text)
area = length * width

print(f"Area: {area} square units")
```

Example interaction:

```text
Length: 5
Width: 3
Area: 15.0 square units
```

### Visual description

A three-stage pipeline shows keyboard strings `"5"` and `"3"`, conversion with `float()`, and numeric values entering multiplication.

### Instructor notes

- Use `type()` to demonstrate the type before and after conversion.
- Ask what might happen if the user types `"wide"` instead of a number.
- Explain that validating incorrect input is a later topic.

### Notebook connection

The notebook converts values between types. This example establishes why conversion is necessary before arithmetic.

### Sources

- [Python Built-in Function: input](https://docs.python.org/3/library/functions.html#input)
- [Python Built-in Function: float](https://docs.python.org/3/library/functions.html#float)

---

## Slide 10 - Errors Fail in Different Ways

### Teaching purpose

Help beginners distinguish syntax, runtime, and logic errors.

### Learner-facing content

An **error** is a problem that prevents a program from working as intended.

Three useful categories are:

- **Syntax error:** the code does not follow Python's grammar, so Python cannot start it.
- **Runtime error:** the code starts, but an operation fails while it is running.
- **Logic error:** the code runs without an error message, but produces the wrong result.

An error message is evidence about what happened. Read the final line first, then inspect the referenced line of code.

### Worked example

**Syntax error**

```python
shape = "Rectangle
```

The closing quotation mark is missing.

**Runtime error**

```python
float("wide")
```

`"wide"` cannot be converted to a number.

**Logic error**

```python
area = length + width
```

The code runs, but addition was used instead of multiplication.

### Code example

Corrected version:

```python
length = 5
width = 3
area = length * width
print(area)
```

Expected output:

```text
15
```

### Visual description

Three side-by-side panels show: code rejected before running, code failing during execution, and code completing with an incorrect answer. Each has one concrete example.

### Instructor notes

- Run each example separately so learners can observe the different behavior.
- Normalize debugging as comparing expected behavior with actual behavior.
- Avoid teaching exception handling yet; it belongs after basic control flow.

### Notebook connection

Notebook work frequently produces tracebacks. Recognizing the error category helps learners decide whether to inspect syntax, data, or reasoning.

### Sources

- [Python Tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Software Carpentry: Built-in Functions and Help](https://swcarpentry.github.io/python-novice-inflammation/02-numpy.html)

---

## Slide 11 - Worked Program: Convert Minutes

### Teaching purpose

Combine input, conversion, variables, arithmetic, and output in a new problem.

### Learner-facing content

Problem: Ask for a duration in minutes, then display the number of complete hours and the remaining minutes.

We need two operators:

- `//` performs whole-number division.
- `%` gives the remainder after division.

Algorithm:

1. Read the total minutes.
2. Convert the input text to an integer.
3. Divide by `60` using `//` to find complete hours.
4. Divide by `60` using `%` to find remaining minutes.
5. Display both results.

This is a new problem, but it uses the same building blocks as the rectangle program.

### Worked example

For `135` total minutes:

1. Complete hours: `135 // 60 = 2`
2. Minutes used by two hours: `2 x 60 = 120`
3. Remaining minutes: `135 - 120 = 15`
4. The remainder operator gives the same result: `135 % 60 = 15`
5. Output: `2 h 15 min`

### Code example

```python
minutes_text = input("Total minutes: ")
total_minutes = int(minutes_text)

hours = total_minutes // 60
minutes = total_minutes % 60

print(f"{hours} h {minutes} min")
```

Example interaction:

```text
Total minutes: 135
2 h 15 min
```

Useful test cases:

| Input | Expected output |
|---:|---|
| `0` | `0 h 0 min` |
| `59` | `0 h 59 min` |
| `60` | `1 h 0 min` |
| `61` | `1 h 1 min` |
| `135` | `2 h 15 min` |

### Visual description

A timeline groups `135` minutes into two complete 60-minute blocks and one 15-minute remainder. The diagram is paired with `//` for groups and `%` for remainder.

### Instructor notes

- Let learners derive the algorithm before revealing the code.
- Trace `135` together, then ask pairs to predict the boundary cases.
- Explain that testing around `60` exposes mistakes that a single test may miss.

### Notebook connection

This exercise checks the prerequisite Python skills needed before learners encounter functions and collections in the source notebook.

### Sources

- [Python Tutorial: Numbers](https://docs.python.org/3/tutorial/introduction.html#numbers)
- [Python Reference: Arithmetic Conversions and Operators](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)

---

## Slide 12 - Trace, Check, and Prepare for Week 2

### Teaching purpose

Assess whether learners can trace a short program and clarify the boundary between Week 1 and Week 2.

### Learner-facing content

Tracing a program means predicting its state and output without immediately running it.

Trace this program for an input of `150`:

```python
total_minutes = 150
hours = total_minutes // 60
minutes = total_minutes % 60
is_long = total_minutes >= 120
print(hours, minutes, is_long)
```

Before Week 2, you should be able to:

- identify program input and output;
- explain what a variable stores;
- recognize integers, floats, strings, and booleans;
- evaluate a short arithmetic expression;
- explain the difference between `=`, `==`, `//`, and `%`;
- trace statements in execution order;
- use `print()`, `input()`, `int()`, and `float()`;
- recognize syntax, runtime, and logic errors.

Week 2 will use these foundations to teach conditions, loops, functions, and collections such as lists and dictionaries.

### Worked example

Trace for `total_minutes = 150`:

1. `hours = 150 // 60` gives `2`.
2. `minutes = 150 % 60` gives `30`.
3. `is_long = 150 >= 120` gives `True`.
4. The output is `2 30 True`.

### Code example

```python
total_minutes = 150
hours = total_minutes // 60
minutes = total_minutes % 60
is_long = total_minutes >= 120

print(hours, minutes, is_long)
```

Expected output:

```text
2 30 True
```

Knowledge check:

1. Why is the result of `input()` a string?
2. What is the difference between `=` and `==`?
3. What values do `61 // 60` and `61 % 60` produce?
4. Which error type produces a wrong answer without stopping the program?

Answers: text is how `input()` returns keyboard data; assignment versus comparison; `1` and `1`; logic error.

### Visual description

A completed trace table for the `150`-minute program sits beside a two-column readiness map: "Can do now" and "Coming in Week 2."

### Instructor notes

- Give learners two minutes to trace independently before discussing answers.
- Ask for reasoning, not only the final output.
- Use incorrect answers to identify which Week 1 concept needs review.

### Notebook connection

Week 1 covers individual values and expressions. Week 2 adds collections and program logic, preparing learners to approach the source notebook's first major sections.

### Sources

- [Python Tutorial: First Steps Towards Programming](https://docs.python.org/3/tutorial/introduction.html#first-steps-towards-programming)
- [Python Standard Types](https://docs.python.org/3/library/stdtypes.html)

---

## Approval Gate

This Markdown is the review source for Week 1. Its wording, examples, and slide order may be revised during review.

No presentation, PDF, narration, video, or LMS asset should be created or replaced until this Markdown is explicitly approved.
