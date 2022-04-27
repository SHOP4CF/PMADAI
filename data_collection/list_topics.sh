#!/bin/bash

KAFKA_HOME="/home/dhorna/dev/tools/kafka/kafka_2.11-1.1.1"

$KAFKA_HOME/bin/kafka-topics.sh --list --zookeeper localhost:2181
