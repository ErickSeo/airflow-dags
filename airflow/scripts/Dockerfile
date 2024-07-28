FROM spark:3.5.0

COPY users_by_city.py /app/users_by_city.py

WORKDIR /app

ADD https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.0.0/delta-spark_2.12-3.0.0.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/io/delta/delta-storage/3.0.0/delta-storage-3.0.0.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.30/aws-java-sdk-1.11.30.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/net/java/dev/jets3t/jets3t/0.9.4/jets3t-0.9.4.jar /opt/spark/jars
USER root

RUN chown -R 185:185 /opt/spark/jars

USER 185