import json
import os
import pandas as pd
from typing import Dict, Any

from eval_to_go.models import H2OGPTELLM 
from eval_to_go.evaluation import score_correctness 

df = pd.read_csv("./sample_data.csv")

def my_callback(result: Dict[str, Any]):
    print(json.dumps(result, indent=4))

llm = H2OGPTELLM(
    url=os.environ.get("H2OGPTE_BASE_URL"),
    api_key=os.environ.get("H2OGPTE_API_KEY"),
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
)

score_correctness(df, llm, inplace=False, callback=my_callback)

print(df)