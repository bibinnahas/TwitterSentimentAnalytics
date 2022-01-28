from pyspark.sql import SparkSession

from twitter.sentiments.twitter_get_sentiments import preprocessing, text_classification

if __name__ == "__main__":
    # create Spark session
    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "127.0.0.1").option("port", "5007").load()

    # Preprocess the data
    words = preprocessing(lines)

    # text classification to define polarity and subjectivity
    words = text_classification(words)
    # .writeStream.format("console").start().awaitTermination()

    words = words.repartition(1)
    query = words.writeStream.queryName("all_tweets") \
        .outputMode("append") \
        .format("csv") \
        .option("path", "../results/parc") \
        .option("checkpointLocation", "../checkpoint/check") \
        .trigger(processingTime='60 seconds') \
        .start().awaitTermination()