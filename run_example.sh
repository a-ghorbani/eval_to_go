#!/bin/bash

# if you have .env defined automatically export all variables
set -a  
source .env
set +a  

python -m eval_to_go.main openai --model gpt-3.5-turbo-0125 ./examples/sample_data.csv output_data.csv --verbose
#python -m eval_to_go.main h2ogpt --model mistralai/Mixtral-8x7B-Instruct-v0.1 ./examples/sample_data.csv output_data.csv --verbose
#python -m eval_to_go.main h2ogpte --model mistralai/Mixtral-8x7B-Instruct-v0.1 ./examples/sample_data.csv output_data.csv --verbose

