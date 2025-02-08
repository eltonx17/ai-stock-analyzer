import sys
import json
import os

sys.path.insert(0, './analyzer')
sys.path.insert(0, './util')

from llm_analyzer import LLMAnalyzer
from sentiments import news_fetcher
from config_reader import read_config
from image_uploader import upload_image_to_cloudinary

config = read_config('app.config')
api_key = config['api_key']
cloud_name = config['cloudinary_cloud_name']
cloudinary_api_key = config['cloudinary_api_key']
cloudinary_api_secret = config['cloudinary_api_secret']
image_path = 'resources/M&M_2025-02-08_13-51-15_ef82e.png'

analyzer = LLMAnalyzer(api_key)

def read_json_prompt(file_path):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path, 'r') as file:
        prompt = json.load(file)
    return prompt

def fetch_news():
    news_json = news_fetcher("Mahindra & Mahindra Ltd")
    
    file_path = os.path.join('prompts', 'sentiment-classifier-prompt.json')
    prompt = read_json_prompt(file_path)
    prompt[0]['content'][1]['text'] = news_json
    analyzer.invoke_llm(prompt)

def process_image_and_invoke_llm(image_url):
    if image_url:
        print(f'Image URL: {image_url}')
        file_path = os.path.join('prompts', 'chart-classifier-prompt.json')
        prompt = read_json_prompt(file_path)
        # Update the image_url in the prompt
        prompt[0]['content'][1]['image_url']['url'] = image_url
        analyzer.invoke_llm(prompt)
    else:
        print("Failed to upload image to Cloudinary.")

if __name__ == "__main__":
    image_url = upload_image_to_cloudinary(image_path, cloud_name, cloudinary_api_key, cloudinary_api_secret)
    #image_url = "https://res.cloudinary.com/dww0kvefs/image/upload/v1738996055/xtkh1i4oaurcnyin2ctt.png"
    news_json = fetch_news()
    process_image_and_invoke_llm(image_url)