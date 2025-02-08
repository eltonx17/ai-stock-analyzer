import sys
import json
import os

sys.path.insert(0, './analyzer')
sys.path.insert(0, './util')

from llm_analyzer import LLMAnalyzer
from sentiments import news_fetcher
from config_reader import read_config
from image_uploader import upload_image_to_cloudinary
from processing_util import sanitize_json, read_json_prompt, compute_final_sentiment, sort_stock_sentiments

config = read_config('app.config')
api_key = config['api_key']
cloud_name = config['cloudinary_cloud_name']
cloudinary_api_key = config['cloudinary_api_key']
cloudinary_api_secret = config['cloudinary_api_secret']
image_path = 'resources/M&M_2025-02-08_13-51-15_ef82e.png'
prompt_dir = os.path.dirname(__file__)

analyzer = LLMAnalyzer(api_key)

def fetch_buzzing_stocks():
    news_json = news_fetcher("Buzzing Stocks Today India")
    
    file_path = os.path.join('prompts', 'buzzing-stocks-extracter-prompt.json')
    prompt = read_json_prompt(prompt_dir, file_path)
    prompt[0]['content'][1]['text'] = news_json
    buzzing_stocks_json = analyzer.invoke_llm(prompt)
    
    sanitized_json = sanitize_json(buzzing_stocks_json)
    
    buzzing_stocks_dict = json.loads(sanitized_json)
    stock_values = [stock_info['value'] for stock_info in buzzing_stocks_dict.values()]
    
    print(stock_values)
    return stock_values

def fetch_news(stock):
    news_json = news_fetcher(stock)
    
    file_path = os.path.join('prompts', 'sentiment-classifier-prompt.json')
    prompt = read_json_prompt(prompt_dir, file_path)
    prompt[0]['content'][1]['text'] = news_json
    sentiment_json = analyzer.invoke_llm(prompt)
    
    return compute_final_sentiment(sentiment_json, stock)

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
    buzzing_stocks = fetch_buzzing_stocks()
    stock_sentiments = []
    for stock in buzzing_stocks:
        print(stock)
        sentiment = fetch_news(stock)
        stock_sentiments.append({"stock": stock, **sentiment})
    
    sorted_stock_sentiments = sort_stock_sentiments(stock_sentiments)
    print(sorted_stock_sentiments)
    #image_url = upload_image_to_cloudinary(image_path, cloud_name, cloudinary_api_key, cloudinary_api_secret)
    #image_url = "https://res.cloudinary.com/dww0kvefs/image/upload/v1738996055/xtkh1i4oaurcnyin2ctt.png"
    #process_image_and_invoke_llm(image_url)
