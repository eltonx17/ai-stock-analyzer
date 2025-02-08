import json
from gnews import GNews

def news_fetcher(stock_ticker):
    google_news = GNews()
    google_news.period = '2d'
    google_news.countries = ['IN']
    stock_news = google_news.get_news(stock_ticker)
    news_list = []
    for news in stock_news:
        title = news['title']
        date = news['published date']
        news_list.append({'title': title, 'published_date': date})
    news_json = json.dumps(news_list, indent=4)
    return news_json