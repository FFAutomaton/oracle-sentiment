import json
import csv
from datetime import datetime, timezone, timedelta
import os
import time
import nltk
nltk.download('vader_lexicon')  ## Download this if you are running the script for the first time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import openai
import requests
from dotenv import load_dotenv
from utils import *
load_dotenv()


class NewsCrawler:
    def __init__(self) -> None:
        # TODO:: business and tech category loop
        # TODO:: run this daily trigger discord webhook
        self.news_api_top_headlines_url = 'https://newsapi.org/v2/top-headlines'
        self.news_api_everything_url = 'https://newsapi.org/v2/everything'
        openai.api_key = os.getenv("OPENAI_APIKEY")
        self.client = openai

    def get_news_from_news_api(self, url, params):
        response = requests.get(url, params=params)
        print(response.status_code)
        data = json.loads(response.text)
        titles = []
        for article in data.get("articles"):
            desc = article.get('description', '')
            titles.append(desc if desc else '')
        return titles

    def create_sentiment_analysis(self, summary):
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(summary)
        # print(summary)
        print('Compound:', sentiment['compound'], 'Positive:', sentiment['pos'], 'Negative:', sentiment['neg'], 'Neutral:', sentiment['neu'])
        if sentiment['compound'] >= 0.05:
            return 1
        elif sentiment['compound'] <= -0.05:
            return -1
        else:
            return 0

    def run(self, start_date):
        params = {
            # 'country': 'us',  ## try commenting this out for analyzing global headlines
            'q': 'crypto',
            'searchIn': 'title,description',
            'from': datetime.strftime(start_date - timedelta(days=1), '%Y-%m-%d'),
            'to': datetime.strftime(start_date, '%Y-%m-%d'),
            'language': 'en',
            'sortBy': 'popularity',
            'apiKey': os.getenv("NEWSAPI_KEY"),
            'pageSize': 80,
            'page': 1
        }
        titles_array = self.get_news_from_news_api(self.news_api_everything_url, params)
        # translated_titles = translate_titles(self, ' '.join(titles_array))
        translated_titles = generate_summary(self, ' '.join(titles_array))
        result = self.create_sentiment_analysis(translated_titles)
        return result


start_date = datetime.strptime('2023-05-19', '%Y-%m-%d').replace(tzinfo=timezone.utc)
end_date = datetime.strptime('2023-05-20', '%Y-%m-%d').replace(tzinfo=timezone.utc)
# end_date = datetime.strptime('2023-05-19', '%Y-%m-%d').replace(tzinfo=timezone.utc)

news_crawler = NewsCrawler()
f = open('./sentiment_descriptions.csv', 'a')
writer = csv.writer(f, delimiter=',', escapechar='', quoting=csv.QUOTE_NONE)


while start_date < end_date:
    flag = news_crawler.run(start_date)
    row = []
    row.append(datetime.strftime(start_date - timedelta(days=1), '%Y-%m-%d'))
    row.append(flag)
    writer.writerow(row)
    # print("#" * 30 + flag + "#" * 30)
    time.sleep(2)
    start_date = start_date + timedelta(days=1)


f.close()