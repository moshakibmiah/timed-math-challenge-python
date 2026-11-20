"""Timed arithmetic practice using only the Python standard library."""

import argparse
import random
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Problem:
    left: int
    operator: str
    right: int

    @property
    def answer(self):
        if self.operator == "+":
            return self.left + self.right
        if self.operator == "-":
            return self.left - self.right
        if self.operator == "*":
            return self.left * self.right
        raise ValueError("Unsupported operator")

    def __str__(self):
        return f"{self.left} {self.operator} {self.right}"


def generate_problem(rng, maximum):
    return Problem(rng.randint(1, maximum), rng.choice(("+", "-", "*")),
                   rng.randint(1, maximum))


def positive_integer(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive whole number") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive whole number")
    return number


def run_quiz(count, maximum, rng=None, read=input, write=print, clock=time.perf_counter):
    """One scored attempt per problem; invalid text is retried and timed."""
    if count < 1 or maximum < 1:
        raise ValueError("Question count and maximum must be positive.")
    rng = rng if rng is not None else random.Random()
    correct = 0
    durations = []
    for index in range(count):
        problem = generate_problem(rng, maximum)
        started = clock()
        while True:
            raw = read(f"[{index + 1}/{count}] {problem} = ").strip()
            if raw.lower() == "q":
                return correct, durations
            try:
                answer = int(raw)
                break
            except ValueError:
                write("Enter a whole number (negative answers are allowed), or q to finish.")
        elapsed = max(0.0, clock() - started)
        durations.append(elapsed)
        if answer == problem.answer:
            correct += 1
            write(f"Correct! ({elapsed:.2f}s)")
        else:
            write(f"Incorrect. The answer was {problem.answer}. ({elapsed:.2f}s)")
    return correct, durations


def main():
    parser = argparse.ArgumentParser(description="Timed addition, subtraction and multiplication practice.")
    parser.add_argument("--questions", type=positive_integer, default=10)
    parser.add_argument("--max-number", type=positive_integer, default=12)
    parser.add_argument("--seed", type=int, help="Reproduce a sequence for practice")
    args = parser.parse_args()
    print("Timed Math Challenge\nAnswer each question once. Enter q to finish early.")
    try:
        input("Press Enter to start...")
        correct, durations = run_quiz(args.questions, args.max_number, random.Random(args.seed))
    except (EOFError, KeyboardInterrupt):
        print("\nChallenge cancelled.")
        return
    completed = len(durations)
    total = sum(durations)
    print(f"\nFinal score: {correct}/{completed} completed ({args.questions} planned)")
    if completed:
        print(f"Accuracy: {correct / completed:.0%}")
        print(f"Total response time: {total:.2f}s")
        print(f"Average response time: {total / completed:.2f}s")
    else:
        print("No questions completed.")


if __name__ == "__main__":
    main()
