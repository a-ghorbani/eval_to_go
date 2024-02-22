from abc import ABC, abstractmethod
from typing import Any, Dict

from h2ogpte import H2OGPTE
from openai import OpenAI


class BaseLLM(ABC):
    """
    Abstract base class for language model clients.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate output based on the given prompt.

        Parameters:
        - prompt (str): The prompt for generation.

        Returns:
        - str: The generated output text.
        """
        pass


class H2OGPTELLM(BaseLLM):
    """
    H2O.ai GPTe language model client.
    """

    def __init__(self, url: str, model: str, api_key: str):
        self.client = H2OGPTE(address=url, api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.answer_question(question=prompt, llm=self.model)
        return response.content


class OpenAILLM(BaseLLM):
    """
    OpenAI language model client.
    """

    def __init__(self, model: str, api_key: str, url: str = None):
        self.client = OpenAI(api_key=api_key)
        if url:
            self.client.base_url = url
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
