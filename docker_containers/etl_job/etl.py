import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#time.sleep(10)  # seconds

def get_sentiment(score):
    sentiment = 'neutral'
    if score >= 0.05:
        sentiment = 'positive'
    elif score <= -0.05:
        sentiment = 'negative'
    return sentiment

# Connect to postgres:
pg = create_engine('postgres://postgres:postgres@postgres:5432/db', echo=True)

#Create table tweets in postgres db:
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    score NUMERIC,
    sentiment VARCHAR(8),
    timestamp NUMERIC
);
''')


# Connect to mongodb:
client = pymongo.MongoClient('mongodb')
db = client.tweet_collector


# Sentimentanalysis
s = SentimentIntensityAnalyzer()

last_timestamp = 0

while True:

    tweets = db.tweets.find({'timestamp': {'$gt': last_timestamp}}) # Extract tweets from mongodb
    print('tweets found: ' + str(tweets.count()))
   
    for tweet in tweets:
        text = tweet['text']
        score = s.polarity_scores(text)['compound']  # placeholder value
        sentiment = get_sentiment(score)
        timestamp = tweet['timestamp']
        query = "INSERT INTO tweets VALUES (%s, %s, %s, %s);"
        pg.execute(query, (text, score, sentiment, timestamp))
        last_timestamp = timestamp
    time.sleep(10.0)





