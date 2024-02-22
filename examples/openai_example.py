import json
import os
import pandas as pd
from typing import Dict, Any

from eval_to_go.models import OpenAILLM
from eval_to_go.evaluation import score_correctness 

df = pd.read_csv("./sample_data.csv")

def my_callback(result: Dict[str, Any]):
    print(json.dumps(result, indent=4))

openai_llm_default = OpenAILLM(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-3.5-turbo-0125",
)
score_correctness(df, openai_llm_default, inplace=True, callback=my_callback)

print(df)
