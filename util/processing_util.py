import json
import os

def sanitize_json(json_string):
    start_index = json_string.find('{')
    end_index = json_string.rfind('}') + 1
    sanitized_json = json_string[start_index:end_index]
    return sanitized_json

def read_json_prompt(prompt_dir, file_path):
    abs_file_path = os.path.join(prompt_dir, file_path)
    with open(abs_file_path, 'r') as file:
        prompt = json.load(file)
    return prompt

def compute_final_sentiment(sentiment_json, stock):
    sanitized_json = sanitize_json(sentiment_json)
    sentiment_dict = json.loads(sanitized_json)
    
    overall_sentiment = sentiment_dict.get("overallSentiment")
    positive = int(sentiment_dict.get("positive", 0))
    negative = int(sentiment_dict.get("negative", 0))
    neutral = int(sentiment_dict.get("neutral", 0))
    
    sentiment_ratios = {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_to_negative_ratio": positive / (negative + 1),  # Avoid division by zero
        "positive_to_neutral_ratio": positive / (neutral + 1)    # Avoid division by zero
    }
    
    print(f"Sentiment ratios for {stock}: {sentiment_ratios}")
    
    if sentiment_ratios["positive"] > 0:
        if sentiment_ratios["positive_to_negative_ratio"] > 2 and sentiment_ratios["positive_to_neutral_ratio"] > 2:
            return {"overall_sentiment": overall_sentiment, "sentiment_ratios": sentiment_ratios}
        elif negative > neutral:
            return {"overall_sentiment": "negative", "sentiment_ratios": sentiment_ratios}
        elif neutral > negative:
            return {"overall_sentiment": "neutral", "sentiment_ratios": sentiment_ratios}
    
    return {"overall_sentiment": "undefined", "sentiment_ratios": sentiment_ratios}

def sort_stock_sentiments(stock_sentiments):
    return sorted(stock_sentiments, key=lambda x: x["sentiment_ratios"]["positive_to_negative_ratio"], reverse=True)
