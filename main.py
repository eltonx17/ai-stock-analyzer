import sys
import json
import os
import webbrowser
import time
import pyautogui

sys.path.insert(0, './analyzer')
sys.path.insert(0, './util')

from llm_analyzer import LLMAnalyzer
from sentiments import news_fetcher
from config_reader import read_config
from image_uploader import upload_image_to_cloudinary
from processing_util import sanitize_json, read_json_prompt, compute_final_sentiment, sort_stock_sentiments
from ticker_mappings import TICKER_MAPPINGS

config = read_config('app.config')
api_key = config['api_key']
cloud_name = config['cloudinary_cloud_name']
cloudinary_api_key = config['cloudinary_api_key']
cloudinary_api_secret = config['cloudinary_api_secret']
prompt_dir = os.path.dirname(__file__)
resources_folder = 'resources'

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
        prompt = read_json_prompt(prompt_dir, file_path)
        # Update the image_url in the prompt
        prompt[0]['content'][1]['image_url']['url'] = image_url
        analyzer.invoke_llm(prompt)
    else:
        print("Failed to upload image to Cloudinary.")

def open_tradingview_charts(stocks):
    base_url = "https://www.tradingview.com/chart/dso7iClB/?symbol=NSE%3A"
    for stock in stocks:
        url = f"{base_url}{stock}"
        webbrowser.open(url)
        time.sleep(5)  # wait for the page to load
        pyautogui.hotkey('alt', 'r')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'alt', 's')
        time.sleep(2)  # wait a bit before opening the next link

def process_images_in_folder(folder_path, cloud_name, cloudinary_api_key, cloudinary_api_secret):
    for image_file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_file)
        if os.path.isfile(image_path):
            image_url = upload_image_to_cloudinary(image_path, cloud_name, cloudinary_api_key, cloudinary_api_secret)
            process_image_and_invoke_llm(image_url)

def extract_positive_stocks(sorted_stock_sentiments):
    positive_stocks = []
    for stock_sentiment in sorted_stock_sentiments:
        if stock_sentiment["overall_sentiment"] == "positive":
            stock_name = stock_sentiment["stock"]
            ticker = TICKER_MAPPINGS.get(stock_name)
            if ticker:
                positive_stocks.append(ticker)
    return positive_stocks

if __name__ == "__main__":
    buzzing_stocks = fetch_buzzing_stocks()
    stock_sentiments = []
    for stock in buzzing_stocks:
        print(stock)
        sentiment = fetch_news(stock)
        stock_sentiments.append({"stock": stock, **sentiment})
    
    sorted_stock_sentiments = sort_stock_sentiments(stock_sentiments)
    print(sorted_stock_sentiments)
    
    positive_stocks = extract_positive_stocks(sorted_stock_sentiments)
    print("Positive stocks with tickers:", positive_stocks)
    
    #stocks_to_view = ['BHARTIARTL', 'HEROMOTOCO', 'SBIN']
    open_tradingview_charts(positive_stocks)
    
    process_images_in_folder(resources_folder, cloud_name, cloudinary_api_key, cloudinary_api_secret)