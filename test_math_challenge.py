import argparse
import random
import unittest

from math_challenge import Problem, generate_problem, positive_integer, run_quiz


class QuizTests(unittest.TestCase):
    def test_arithmetic_including_negative_subtraction(self):
        for operator, answer in (("+", 8), ("-", -2), ("*", 15)):
            self.assertEqual(Problem(3, operator, 5).answer, answer)

    def test_generated_operands_and_operators(self):
        rng = random.Random(7)
        seen = set()
        for _ in range(100):
            p = generate_problem(rng, 12)
            self.assertTrue(1 <= p.left <= 12 and 1 <= p.right <= 12)
            seen.add(p.operator)
        self.assertEqual(seen, {"+", "-", "*"})

    def test_scoring_and_timing_with_invalid_input(self):
        seed = 10
        rng = random.Random(seed)
        first = generate_problem(rng, 12)
        second = generate_problem(rng, 12)
        answers = iter(["invalid", str(first.answer), str(second.answer + 1)])
        ticks = iter([10.0, 12.0, 15.0, 18.0])
        score, times = run_quiz(2, 12, random.Random(seed),
                                lambda _: next(answers), lambda _: None,
                                lambda: next(ticks))
        self.assertEqual(score, 1)
        self.assertEqual(times, [2.0, 3.0])

    def test_quit_does_not_count_unanswered_question(self):
        self.assertEqual(run_quiz(3, 12, read=lambda _: "q"), (0, []))

    def test_positive_argument_validation(self):
        for value in ("0", "-1", "abc", "1.5"):
            with self.assertRaises(argparse.ArgumentTypeError):
                positive_integer(value)


if __name__ == "__main__":
    unittest.main()
