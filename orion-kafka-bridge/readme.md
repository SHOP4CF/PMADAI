# Orion-kafka bridge

```
docker build -t  orion_kafka_bridge .

docker run -d -p 5000:5000 orion_kafka_bridge

curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/notify
```

API Walkthrough:
https://fiware-orion.readthedocs.io/en/1.15.1/user/walkthrough_apiv2/

### PMADAI entities:
Add entity:
```
curl localhost:1026/v2/entities -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "id": "current_on_busbar_1",
  "type": "CurrentTrends",
  "timestamp": {
    "value": "2020-09-30 22:05:11.330000",
    "type": "String"
  },
  "value": {
    "value": 6.076,
    "type": "Float"
  }
}
EOF
```

Update entity:
```
curl localhost:1026/v2/entities/current_on_busbar_1/attrs -s -S -H 'Content-Type: application/json' -X PATCH -d @- <<EOF
{
  "timestamp": {
    "value": "2020-09-30 22:05:12.330000",
    "type": "String"
  },
  "value": {
    "value": 7.076,
    "type": "Float"
  }
}
EOF
```

Set up subscription:
```
curl -v localhost:1026/v2/subscriptions -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "description": "A subscription to get info about Room1",
  "subject": {
    "entities": [
      {
        "id": "current_on_busbar_1",
        "type": "CurrentTrends"
      }
    ],
    "condition": {
      "attrs": [
        "timestamp",
        "value"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://172.17.0.1:5000/notify"
    },
    "attrs": [
      "timestamp",
      "value"
    ]
  },
  "expires": "2040-01-01T14:00:00.00Z",
  "throttling": 1
}
EOF
```

Useful commands:
```
bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic CurrentTrends
bin/kafka-topics.sh --list --zookeeper localhost:2181
bin/kafka-console-consumer.sh --topic CurrentTrends --from-beginning --bootstrap-server localhost:9092
```