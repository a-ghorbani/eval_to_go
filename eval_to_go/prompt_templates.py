default_prompt_template = """
You are tasked with evaluating the accuracy and relevance of a response provided by a GPT model. 
Below, you will find a specific question, the GPT model's response to that question, and the actual, verified information (referred to as 'Ground Truth'). 
Your job is to compare the essence of the GPT model's response with the Ground Truth to determine if the response accurately addresses the question. 
Minor discrepancies in format, like rounding in numerical values, order of values, or additional relevant information provided by the model should not be considered incorrect if they do not misrepresent the Ground Truth. 
Please provide your evaluation in a JSON format: 
{{
    "Response": true/false,
    "Reason": "[Explain here. If true, you may state 'Accurate and relevant.' If false, detail the specific inaccuracies or irrelevances.]",
}}

Question asked to the GPT model: {question}

GPT model's response: '{answer}'

Ground Truth information: '{ground_truth}'

Based on the Ground Truth, determine the accuracy and relevance of the GPT model's response. Your output should have no additional text than the specified JSON output.
"""
