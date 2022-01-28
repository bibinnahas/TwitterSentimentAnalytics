from textblob import TextBlob

import pyspark
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import col, array_contains, explode, split, udf
from pyspark.sql.types import StringType


def preprocessing(lines):
    words = lines.select(explode(split(lines.value, "t_end")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    words = words.withColumn('word', F.regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '#', ''))
    words = words.withColumn('word', F.regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', F.regexp_replace('word', ':', ''))
    return words


# text classification
def polarity_detection(text):
    return TextBlob(text).sentiment.polarity


def subjectivity_detection(text):
    return TextBlob(text).sentiment.subjectivity


def text_classification(words):
    # polarity detection
    polarity_detection_udf = udf(polarity_detection, StringType())
    words = words.withColumn("polarity", polarity_detection_udf("word"))
    # subjectivity detection
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    words = words.withColumn("subjectivity", subjectivity_detection_udf("word"))
    return words


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
        .option("path", "./parc") \
        .option("checkpointLocation", "./check") \
        .trigger(processingTime='60 seconds') \
        .start().awaitTermination()
