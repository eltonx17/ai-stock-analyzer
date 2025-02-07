import json
import os
from openai import OpenAI

class ChartAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def analyze_image(self, image_url):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../prompts/chart-classifier-prompt.json')

        # Read the JSON prompt template
        with open(file_path, 'r') as file:
            messages = json.load(file)
        # Update the image_url in the prompt
        messages[0]['content'][1]['image_url']['url'] = image_url

        completion = self.client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="google/gemini-2.0-pro-exp-02-05:free",
            messages=messages
        )
        if not completion or not completion.choices:
            print("Chart Error: No response from the API.")
            print(completion)  # Debugging
        else:
            print(completion.choices[0].message.content)