#!/bin/bash

KAFKA_HOME="........./dev/tools/kafka/kafka_2.11-1.1.1"

topics=("Metadata" "SMT" "Jobs" "PositionTrends" "VoltageTrends" "CurrentTrends" "ChargeTrends" "PreprocessingResults", "Alerts")


for topic in ${topics[@]}; do
  # delete topic
  $KAFKA_HOME/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic $topic

  # create topic
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic $topic
done