# Timed Math Challenge (Python)

A console arithmetic quiz that generates random addition, subtraction, and multiplication questions, measures response times, and reports a final score. Uses Python's `random` and `time` modules with no external dependencies.

## Run

Requires Python 3.10 or later. From this folder:

```sh
python math_challenge.py
```

On Windows, `py math_challenge.py` also works if the Python launcher is installed.

Press Enter to start a ten-question quiz. Each operand is between 1 and 12 by default. Subtraction can produce negative answers.

## Options

```sh
python math_challenge.py --questions 5 --max-number 20
python math_challenge.py --questions 5 --seed 42
python math_challenge.py --help
```

`--seed` reproduces a sequence of questions for practice. Question count and maximum operand must be positive whole numbers.

## Scoring and timing

- Each question accepts one numeric attempt. A wrong answer reveals the solution and moves on.
- Invalid text prompts another attempt on the same question; the timer continues.
- Enter `q` at an answer prompt to finish early and see your results.
- Score is the number correct out of the questions completed. Accuracy is correct divided by completed.
- The report includes total response time and average time per completed question.
- Timing uses `time.perf_counter`, a monotonic clock. It starts when a question is presented and stops when a valid numeric answer is entered. Feedback and the initial start prompt are excluded.
- An unanswered question is excluded from both score and timing if you quit.

This is a stopwatch-style challenge: there is no countdown or forced time limit. Ctrl+C or end-of-input cancels the session.

## Test

```sh
python -m unittest discover -v
```

Tests cover arithmetic, generated operand bounds and operators, scoring, deterministic timing, invalid input, early exit, and argument validation. GitHub Actions runs them on Python 3.10 and 3.13.

## Code guide

- `Problem`: stores an arithmetic expression and computes its answer without `eval`.
- `generate_problem`: creates an expression using a random number generator.
- `run_quiz`: manages questions, input validation, scoring, and response times.
- `main`: handles command-line options and displays the results.
