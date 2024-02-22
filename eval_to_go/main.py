import argparse
import json
import os
import pandas as pd
from typing import Dict, Any
from .models import OpenAILLM, H2OGPTELLM 
from .evaluation import score_correctness


def my_callback(result: Dict[str, Any]):
    print(json.dumps(result, indent=4))


def calculate_true_rate(df, column_name="eval_result"):
    filtered_df = df.dropna(subset=[column_name])
    true_count = filtered_df[column_name].sum()
    true_rate = true_count / len(filtered_df) if len(filtered_df) > 0 else 0
    return true_rate


def main(
    provider: str, model: str, input_file: str, output_file: str, verbose: bool = False
):
    df = pd.read_csv(input_file)

    if provider.lower() == "openai":
        llm = OpenAILLM(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model=model or "gpt-3.5-turbo-0125",
        )
    elif provider.lower() == "h2ogpt":
        llm = OpenAILLM(
            url=os.environ.get("H2OGPT_BASE_URL"),
            api_key=os.environ.get("H2OGPT_API_KEY"),
            model=model
            or "mistralai/Mixtral-8x7B-Instruct-v0.1",
        )
    elif provider.lower() == "h2ogpte":
        llm = H2OGPTELLM(
            url=os.environ.get("H2OGPTE_BASE_URL"),
            api_key=os.environ.get("H2OGPTE_API_KEY"),
            model=model
            or "mistralai/Mixtral-8x7B-Instruct-v0.1",
        )
    else:
        raise ValueError(
            "Unsupported provider. Choose from 'openai', 'h2ogpt', or 'h2ogpte'."
        )

    score_correctness(df, llm, inplace=True, callback=my_callback if verbose else None)

    print("Success Rate: ", calculate_true_rate(df))

    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate correctness with LLM.")
    parser.add_argument(
        "provider", help="Provider of the LLM. Options: openai, h2ogpt, h2ogpte"
    )
    parser.add_argument(
        "--model",
        help="Model identifier. Optional, defaults vary by provider.",
        default="",
    )
    parser.add_argument("input_file", help="Input CSV file path.")
    parser.add_argument("output_file", help="Output CSV file path.")
    parser.add_argument(
        "--verbose", help="Increase output verbosity.", action="store_true"
    )

    args = parser.parse_args()

    main(args.provider, args.model, args.input_file, args.output_file, args.verbose)
