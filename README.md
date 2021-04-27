# tweetbot-pipeline
Dockerized pipeline that collects tweets from Twitter related to a chosen topic and stores them in MongoDB, analyzes the sentiment of each tweet, stores analyzed tweets in PostgresDB and posts tweets with sentiment score binned as positive, neutral or negative to a slack channel.
