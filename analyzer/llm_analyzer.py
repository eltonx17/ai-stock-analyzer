from openai import OpenAI

class LLMAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def invoke_llm(self, prompt):

        completion = self.client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="google/gemini-2.0-flash-exp:free",
            messages=prompt
        )
        if not completion or not completion.choices:
            print("LLM Analyzer Error: No response from the API.")
            print(completion)  # Debugging
        else:
            print(completion.choices[0].message.content)

#model="google/gemini-2.0-pro-exp-02-05:free",