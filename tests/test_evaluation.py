import unittest
from unittest.mock import patch
from pandas import DataFrame

from eval_to_go.evaluation import score_correctness
from eval_to_go.models import BaseLLM


class MockLLM(BaseLLM):
    def generate(self, prompt: str) -> str:
        # Mock response generation logic
        # This could return fixed responses based on the prompt for testing
        return '{"Response": true, "Reason": "Mocked response accurate."}'


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        # Setup mock DataFrame for testing
        self.df = DataFrame(
            {
                "question": ["What is the capital of France?"],
                "answer": ["Paris"],
                "ground_truth": ["Paris"],
            }
        )

    @patch("eval_to_go.evaluation.BaseLLM", new=MockLLM)
    def test_score_correctness(self):
        # Initialize the mock LLM
        mock_llm = MockLLM()

        # Execute the scoring function
        result_df = score_correctness(self.df, mock_llm, False)

        # Check if the result DataFrame contains the expected evaluation result
        self.assertTrue(result_df.loc[0, "eval_result"])
        self.assertEqual(result_df.loc[0, "eval_reason"], "Mocked response accurate.")


if __name__ == "__main__":
    unittest.main()
