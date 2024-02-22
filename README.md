# Eval To Go

A no-fuss eval tool for zapping through RAG and LLM evaluations!
It is a loose version of correctness evaluation in RAGAS framework.
Written for the busy folks like myself who are just too swamped to deal with the setup of professional eval tools.
As a result `eval_to_go` is by no means a comprehensive, complete evaluation tool. 
Instead, it's a simple way to get evaluations done in just a few lines of code, like when you need an eval in a PoC that was due yesterday.

In other words, you may well encounter cases that are not covered. 
However, it provides a foundation for evals based on another LLM acting as a judge, by modifying the prompt template or LLM output format, among other things.

For serious projects, consider using more appropriate tools such as the RAGAS framework or enterprise implementations like H2O.ai's Eval Studio.

## Getting Started

### Installation

Get up and running with `Eval To Go`:

```bash
pip install eval_to_go
```

## Usage

`Eval To Go` supports both command-line and script-based interactions. Below are examples to kickstart your evaluation process:

## Input File Format

Your input dataset must be structured in a CSV format with specific columns:

- **question**: The question intended to be answered by your RAG or LLM.
- **ground_truth**: The main essence of the expected response, which could be a single word or a short phrase.
- **answer**: The actual response provided by your RAG or LLM to the question.

Below is an example of how your input CSV file should be structured:

| question                                                                 | ground_truth                                                                                                | answer                                                                                                      |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| What was the actual value of the customer satisfaction in 2022?          | 0.75                                                                                                        | The actual value of the customer satisfaction metric in 2022 was 0.83.                                      |
| What was the target value for the customer satisfaction metric in 2022? | 0.7                                                                                                         | The target value for the customer satisfaction metric in 2022 was 0.70.                                     |
| What is Firm GmbH's number of customer accounts as of 31 December 2022?  | 97945                                                                                                       | As of 31 December 2022, Firm GmbH had a total of 97,945 customer accounts.                                  |
| What are Firm GmbH's values?                                             | Integrity, Transparency, Customer-Centricity, Sustainability, Social Responsibility                         | Firm GmbH values Customer-Centricity, Integrity, Transparency, Sustainability, and Social Responsibility.   |

---

### Using OpenAI

#### Command Line

```sh
python -m eval_to_go.main openai --model gpt-3.5-turbo-0125 ./examples/sample_data.csv output_data.csv --verbose
```

#### In a Python Script

```python
import os
import pandas as pd
from typing import Dict, Any

from eval_to_go.models import OpenAILLM
from eval_to_go.evaluation import score_correctness 

# Load your data
df = pd.read_csv("./sample_data.csv")

# Define a callback to process results
def my_callback(result: Dict[str, Any]):
    print(json.dumps(result, indent=4))

# Configure the LLM
openai_llm = OpenAILLM(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-3.5-turbo-0125",
)

# Perform evaluation
score_correctness(df, openai_llm, inplace=True, callback=my_callback)

# Review results
print(df)
```

### Evaluating with h2oGPT and Enterprise h2oGPT Models

Similar to the OpenAI example, you can use `Eval To Go` for evaluation using h2oGPT models as the judges. See the `examples` dir or `run_example.sh` for the additional examples.

### Expected Output

At completion of the evaluation, the input dataset will have two additional columns to provide insights into the evaluation results:

- `eval_result`: A Boolean value indicating whether the LLM's answer  matches the ground truth (True) or not (False).
- `eval_reason`: A brief rationale behind the `eval_result` value.

Here's how the output would look like for the sample dataset provided:

| question                                                                 | ground_truth                                                                                                | answer                                                                                                      | eval_result | eval_reason                                                                                   |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------|---------------------------------------------------------------------------------------------|
| What was the actual value of the customer satisfaction in 2022?          | 0.75                                                                                                        | The actual value of the customer satisfaction metric in 2022 was 0.83.                                      | False       | The GPT model's response (0.83) does not match the Ground Truth (0.75).                      |
| What was the target value for the customer satisfaction metric in 2022? | 0.7                                                                                                         | The target value for customer satisfaction metric in 2022 was 0.70.                                         | True        | Accurate and relevant.                                                                        |
| What is Firm GmbH's number of customer accounts as of 31 December 2022?  | 97945                                                                                                       | 97,945                                                                                                      | True        | Accurate and relevant.                                                                        |
| What are Firm GmbH's values?                                             | • Integrity • Transparency • Customer-Centricity • Sustainability • Social Responsibility                   | Firm GmbH's values are Customer-Centricity, Integrity, Transparency, Sustainability, Social Responsibility | True        | Accurate and relevant.                                                                        |


## Contributing

Contributions to `Eval To Go` are welcomed, whether it's through bug reports, code enhancements, documentation improvements, or feature requests. 

## License

`Eval To Go` is made available under the [MIT License](LICENSE). For more details, see the LICENSE file in the project repository.