import requests
import os
import json
from services.news_crawler import NewsCrawler, prepare_message_daily, prepare_message_15m
from services.aylien_crawler import AylienCrawler
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import time
import csv

load_dotenv()


def main():
    start_date = datetime.utcnow()
    if start_date.hour == 4 and start_date.minute == 0:
        news_crawler = NewsCrawler()
        summary, flag = news_crawler.run(start_date)

        data = prepare_message_daily(summary, flag, start_date)
        requests.post(
            os.getenv("BORG_AGENT_WEBHOOK"), headers={"Content-Type": "application/json"}, data=json.dumps(data)
        )

    # aylien_crawler = AylienCrawler()
    # titles, alert = aylien_crawler.fetch_new_stories_titles()
    # if alert != 0:
    #
    #     data = prepare_message_15m(titles, alert, start_date)
    #     requests.post(
    #         os.getenv("BORG_AGENT_WEBHOOK"), headers={"Content-Type": "application/json"}, data=json.dumps(data)
    #     )


def backfill():
    start_date = datetime.strptime('2023-05-19', '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end_date = datetime.strptime('2023-05-20', '%Y-%m-%d').replace(tzinfo=timezone.utc)

    news_crawler = NewsCrawler()
    f = open('./sentiment_descriptions.csv', 'a')
    writer = csv.writer(f, delimiter=',', escapechar='', quoting=csv.QUOTE_NONE)

    while start_date < end_date:
        summary, flag = news_crawler.run(start_date)
        row = []
        row.append(datetime.strftime(start_date - timedelta(days=1), '%Y-%m-%d'))
        row.append(flag)
        writer.writerow(row)
        # print("#" * 30 + flag + "#" * 30)
        time.sleep(2)
        start_date = start_date + timedelta(days=1)

    f.close()

main()