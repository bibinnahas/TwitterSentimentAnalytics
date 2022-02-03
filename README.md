# Twitter Sentiment Analysis

This repo is under construction and is not in its final form. This was me just trying to consume tweets and present in a clean manner for learning sentiment analysis

## Files
- get_connection.py:- Gets connection and pulls tweets with the word supplied. These tweets will be pushed to the socket port and is ready to be read by the Spark consumer
- get_sentiments.py:- Consumes tweets from the socket port and clenses data to a presentable form

## Directions to run
- Update word in send_tweets method in twitter_get_connection.py
- Update credentials in credentials/twitter_get_credentials.py