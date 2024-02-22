import json
import pandas as pd
from pandas import DataFrame
from typing import Callable, Optional, Dict, Any
from .prompt_templates import default_prompt_template
from .models import BaseLLM


def score_correctness(
    df: DataFrame,
    llm: BaseLLM,
    inplace: bool = True,
    prompt_template: Optional[str] = None,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Optional[DataFrame]:
    """
    Evaluate the correctness of answers based on a given DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame containing questions, answers, and ground truths.
    - llm (BaseLLM): Language model for generating evaluations.
    - inplace (bool): Whether to modify the DataFrame in place.
    - prompt_template (Optional[str], default=None): Template for evaluation prompts. If None, a default template will be used.
    - callback (Callable[[Dict[str, Any]], None], optional): Callback function for each evaluation result.

    Returns:
    - Optional[DataFrame]: The modified DataFrame if not inplace, otherwise None.
    """
    if not inplace:
        df = df.copy()

    if prompt_template is None:
        prompt_template = default_prompt_template

    df["eval_result"] = pd.Series(dtype="bool")
    df["eval_reason"] = pd.Series(dtype="object")

    for index, row in df.iterrows():
        try:
            eval_prompt = prompt_template.format(
                question=row["question"],
                answer=row["answer"],
                ground_truth=row["ground_truth"],
            )
            result = json.loads(llm.generate(eval_prompt))
            eval_result, eval_reason = result.get("Response"), result.get("Reason")

            df.at[index, "eval_result"] = eval_result
            df.at[index, "eval_reason"] = eval_reason

            if callback:
                callback_data = {
                    "df_index": index,
                    "question": row["question"],
                    "ground_truth": row["ground_truth"],
                    "answer": row["answer"],
                    "eval_result": eval_result,
                    "eval_reason": eval_reason,
                }
                callback(callback_data)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            df.at[index, "eval_result"] = None
            df.at[index, "eval_reason"] = error_message
            if callback:
                callback({"df_index": index, "error": error_message})

    return df if not inplace else None
