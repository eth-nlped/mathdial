import unittest

from interactivetutoring.evaluate import get_match, evaluate_at_k


class TestMetrics(unittest.TestCase):

    def test_match_answer_in_text(self):
        given_answer = "Sure! I think Tammy has gotten 70 haircuts in total. Here's how I got my answer: I know that for every 14 haircuts, Tammy gets a free one. So if she's gotten 5 free haircuts already, that means she's gotten 5 groups of 14 haircuts, or 70 haircuts in total. She's also 5 haircuts away from her next free one, which means she's gotten 79 haircuts without a free one. "
        ground_truth = "79"
        self.assertEqual(True, get_match(given_answer, ground_truth))

        given_answer = "Sure! He has to pay $20 more, not $30."
        ground_truth = "20"
        self.assertEqual(True, get_match(given_answer, ground_truth))

    def test_evaluate_at_k(self):
        utterances_list = ["Teacher: Can you walk me through?",
                           "Student: This is my solution: 2+3=5",
                           # round 1
                           "Teacher: I don't think it is correct, why did you include 2?",
                           "Student: Oh I see, sorry for my incorrect answer.",
                           # round 2
                           "Teacher: What is the answer?",
                           "Student: My corrected asnwer is is 2+4=6",
                           # round 3
                           "Teacher: Good job, you are right, the answer is 6.",
                           "Student: Thanks"
                           ]
        answer = "6"
        k = 1
        success_at_k, telling_at_k = evaluate_at_k(utterances_list, answer, k)
        self.assertEqual(False, success_at_k)
        self.assertEqual(False, telling_at_k)

        k = 2
        success_at_k, telling_at_k = evaluate_at_k(utterances_list, answer, k)
        self.assertEqual(True, success_at_k)
        self.assertEqual(False, telling_at_k)

        k = 3
        success_at_k, telling_at_k = evaluate_at_k(utterances_list, answer, k)
        self.assertEqual(True, success_at_k)
        self.assertEqual(False, telling_at_k)

        utterances_list = ["Teacher: Can you walk me through?",
                           "Student: This is my solution: 2+3=5",
                           # round 1
                           "Teacher: I don't think it is correct, why did you include 2?",
                           "Student: Oh I see, sorry for my incorrect answer.",
                           # round 2
                           "Teacher: I'll tell you the answer, it is 6. Just do 2+4",
                           "Student: Thanks",
                           # round 3
                           "Teacher: You are welcome",
                           "Student: Bye. I will remember the answer is 6."
                           ]
        answer = "6"
        k = 1
        success_at_k, telling_at_k = evaluate_at_k(utterances_list, answer, k)
        self.assertEqual(False, success_at_k)
        self.assertEqual(False, telling_at_k)

        k = 2
        success_at_k, telling_at_k = evaluate_at_k(utterances_list, answer, k)
        self.assertEqual(False, success_at_k)
        self.assertEqual(True, telling_at_k)

        k = 3
        success_at_k, telling_at_k = evaluate_at_k(utterances_list, answer, k)
        self.assertEqual(True, success_at_k)
        self.assertEqual(True, telling_at_k)
