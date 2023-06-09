url = 'https://api.aylien.com/news/stories?aql=language:(en) AND title: (crypto, sec, binance, huobi, gate.io, bitcoin, ethereum, token, blockchain) AND sentiment.title.polarity:(negative positive)&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY'
import time
import aylien_news_api
from aylien_news_api.rest import ApiException
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class AylienCrawler:
  def __init__(self):
    configuration = aylien_news_api.Configuration()
    configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '4dd67b91'
    configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '02c6eec7c2e6adcc74e1f772773b68a7'
    configuration.host = "https://api.aylien.com/news"

    self.api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))
    self.params = {
      'language': ['en'],
      'aql': 'title:("crypto"^2 OR "binance" OR "huobi" OR "gate.io" OR "bitcoin" OR "ethereum" OR "blockchain" OR "coinbase")',
      'published_at_start': 'NOW-15MINUTES',
      # 'published_at_start': 'NOW-1DAY',
      'published_at_end': 'NOW',
      'cursor': '*',
      'source_rankings_alexa_rank_min': 10,
      'source_rankings_alexa_rank_max': 100,
      'per_page': 100,
      'sort_by': 'recency'
    }

  def fetch_new_stories_titles(self):
    response = self.api_instance.list_stories(**self.params)
    stories = response.stories
    titles = []
    for story in stories:
      if story.sentiment.body.polarity != "neutral":
        titles.append(story.title)
    titles = ' '.join(titles)
    alert = self.create_sentiment_analysis(titles)
    return titles, alert

  def create_sentiment_analysis(self, summary):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(summary)
    # print(summary)
    print('Compound:', sentiment['compound'], 'Positive:', sentiment['pos'], 'Negative:', sentiment['neg'], 'Neutral:',
          sentiment['neu'])
    if sentiment['compound'] >= 0.05:
      return 1
    elif sentiment['compound'] <= -0.05:
      return -1
    else:
      return 0






