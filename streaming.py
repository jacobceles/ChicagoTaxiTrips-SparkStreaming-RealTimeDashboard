"""
Questions:
1. Rate of tipping over years?
2. Popular taxi trips days?
3. Mode of payment over years?
4. Total miles travelled across years?
5. Total time travelled across years?
6. Which company makes the most trips per year?
"""
import requests
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat, lit, to_timestamp, year, month, dayofmonth, to_date


def define_schema():
    labels = [('Trip ID', StringType()),
              ('Taxi ID', StringType()),
              ('Trip Start Timestamp', StringType()),
              ('Trip End Timestamp', StringType()),
              ('Trip Seconds', DoubleType()),
              ('Trip Miles', DoubleType()),
              ('Pickup Census Tract', DoubleType()),
              ('Dropoff Census Tract', DoubleType()),
              ('Pickup Community Area', DoubleType()),
              ('Dropoff Community Area', DoubleType()),
              ('Fare', DoubleType()),
              ('Tips', DoubleType()),
              ('Tolls', DoubleType()),
              ('Extras', DoubleType()),
              ('Trip Total', DoubleType()),
              ('Payment Type', StringType()),
              ('Company', StringType()),
              ('Pickup Centroid Latitude', StringType()),
              ('Pickup Centroid Longitude', StringType()),
              ('Pickup Centroid Location', StringType()),
              ('Dropoff Centroid Latitude', StringType()),
              ('Dropoff Centroid Longitude', StringType()),
              ('Dropoff Centroid  Location', StringType(),
              ('Month', IntegerType()))]
    return StructType([StructField(x[0], x[1], True) for x in labels])


def foreach_batch_function(df, epoch_id):
    request_data = {}
    if 'total_tips' in df.columns:
        labels = [str(t.year) for t in df.select("year").collect()]
        data = [p.total_tips for p in df.select("total_tips").collect()]
        request_data = {'labels0': str(labels), 'values0': str(data)}
    elif 'total_taxi_trip' in df.columns:
        labels = [str(t.date) for t in df.select("date").collect()]
        data = [p.total_taxi_trip for p in df.select("total_taxi_trip").collect()]
        request_data = {'labels1': str(labels), 'values1': str(data)}
    elif 'count_per_category' in df.columns:
        payment_type = df.head()[0].lower()
        labels = [str(t.year) for t in df.select("year").collect()]
        data = [p.count_per_category for p in df.select("count_per_category").collect()]
        if payment_type == "cash":
            request_data = {'labels2': str(labels), 'values2_1': str(data)}
        elif payment_type == "credit card":
            request_data = {'labels2': str(labels), 'values2_2': str(data)}
        else:
            print("Invalid type: " + str(payment_type))
    elif 'total_trip_miles' in df.columns:
        labels = [str(t.year) for t in df.select("year").collect()]
        data = [p.total_trip_miles for p in df.select("total_trip_miles").collect()]
        request_data = {'labels3': str(labels), 'values3': str(data)}
    elif 'total_trip_hours' in df.columns:
        labels = [str(t.year) for t in df.select("year").collect()]
        data = [p.total_trip_hours for p in df.select("total_trip_hours").collect()]
        request_data = {'labels4': str(labels), 'values4': str(data)}
    elif 'total_rides' in df.columns:
        df_temp1 = df.groupBy('year').max("total_rides").select("max(total_rides)")\
            .withColumnRenamed("max(total_rides)", "total_rides_count")
        df_temp2 = df.join(df_temp1, df.total_rides == df_temp1.total_rides_count, "inner")\
            .select(concat(col("year"), lit(": "), col("company")).alias("name"), "total_rides")
        labels = [str(t.name) for t in df_temp2.select("name").collect()]
        data = [p.total_rides for p in df_temp2.select("total_rides").collect()]
        request_data = {'labels5': str(labels), 'values5': str(data)}
    # initialize and send the data through REST API
    url = 'http://localhost:5001/updateData'
    print(request_data)
    requests.post(url, data=request_data)


if __name__ == "__main__":
    spark = SparkSession.builder.appName("Chicago Taxi Trip Streaming Analysis").getOrCreate()
    spark.sparkContext.setLogLevel("FATAL")

    schema = define_schema()
    dataframe = spark.readStream.format("csv").schema(schema)\
        .option("header", True).option("cleanSource", "off")\
        .option("ignoreLeadingWhiteSpace", True).option("mode", "dropMalformed")\
        .option("maxFilesPerTrigger", 1).load("H:/Project 1/source/")

    # Cleaning
    dataframe = dataframe.toDF(*[c.lower().replace(" ", "_") for c in dataframe.columns]) \
        .withColumn('trip_start_timestamp', to_timestamp(col('trip_start_timestamp'), 'MM/dd/yyyy hh:mm:ss a')) \
        .withColumn('trip_end_timestamp', to_timestamp(col('trip_end_timestamp'), 'MM/dd/yyyy hh:mm:ss a')) \
        .withColumn('date', to_date(col('trip_start_timestamp')))\
        .withColumn('year', year(col('trip_start_timestamp')))\
        .withColumn('month', month(col('trip_start_timestamp')))\
        .withColumn('day', dayofmonth(col('trip_start_timestamp')))\
        .na.drop(subset=["Company"])

    # Create a view
    dataframe.createOrReplaceTempView("taxi_trips")

    # 1. Rate of tipping over years?
    spark.sql("""SELECT year, SUM(tips) AS total_tips FROM taxi_trips GROUP BY year""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()

    # 2. Popular taxi trips days?
    spark.sql("""SELECT date, COUNT(trip_id) AS total_taxi_trip FROM taxi_trips GROUP BY date""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()

    # 3. Mode of payment over year
    spark.sql("""SELECT payment_type, year, COUNT(trip_id) AS count_per_category FROM taxi_trips
    GROUP BY payment_type, year HAVING lower(payment_type)=='cash'""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()
    spark.sql("""SELECT payment_type, year, COUNT(trip_id) AS count_per_category FROM taxi_trips
    GROUP BY payment_type, year HAVING lower(payment_type)=='credit card'""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()

    # 4. Total miles taxis travelled across years?
    spark.sql("""SELECT year, SUM(trip_miles) AS total_trip_miles FROM taxi_trips GROUP BY year""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()

    # 5. Total time travelled across years?
    spark.sql("""SELECT year, SUM(trip_seconds)/3600 AS total_trip_hours FROM taxi_trips GROUP BY year""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()

    # 6. Which company makes the most trips per year?
    spark.sql("""SELECT year, company, COUNT(*) as total_rides FROM taxi_trips GROUP BY year, company""")\
        .writeStream.outputMode("complete").foreachBatch(foreach_batch_function).start()

    # Stop only when I say so
    spark.streams.awaitAnyTermination()
