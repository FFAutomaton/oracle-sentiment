# Import the necessary libraries
import json
import os
import nltk
nltk.download('vader_lexicon')  ## Download this if you are running the script for the first time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import openai
import requests
from dotenv import load_dotenv

load_dotenv()


class NewsCrawler:
    def __init__(self) -> None:
        # TODO:: business and tech category loop
        # TODO:: run this daily trigger discord webhook
        self.news_api_url = 'https://newsapi.org/v2/top-headlines'
        openai.api_key = os.getenv("OPENAI_APIKEY")
        self.client = openai

    def get_top_headlines(self):
        params = {
            # 'country': 'us',  ## try commenting this out for analyzing global headlines
            'category': 'technology',
            'apiKey': os.getenv("NEWSAPI_KEY"),
            'pageSize': 100
        }
        response = requests.get(self.news_api_url, params=params)
        data = json.loads(response.text)
        titles = []
        for article in data['articles']:
            titles.append(article['title'])
        return titles

    def translate_titles(self, input_text):
        prompt = f"Please translate the following text to English:\n{input_text}\nTranslation:"
        response = self.client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ]
        )
        summary = response.choices[0].message.content
        return summary

    def generate_summary(self, input_text):
        prompt = f"Please summarize the following text:\n{input_text}\nSummary:"
        response = self.client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ]
        )
        summary = response.choices[0].message.content
        return summary

    def create_sentiment_analysis(self, summary):

        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(summary)

        # Print the results
        print(summary)
        print('Sentiment Analysis Results:')
        print('Positive:', sentiment['pos'])
        print('Negative:', sentiment['neg'])
        print('Neutral:', sentiment['neu'])
        print('Compound:', sentiment['compound'])
        if sentiment['compound'] >= 0.05:
            return "Positive"
        elif sentiment['compound'] <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    def run(self):
        titles_array = self.get_top_headlines()
        translated_titles = self.translate_titles(' '.join(titles_array))
        # translated_titles = self.generate_summary(translated_titles)
        result = self.create_sentiment_analysis(translated_titles)
        return result


flag = NewsCrawler().run()
print("#" * 30 + flag + "#" * 30)

