import json
import requests

import kafka.client
import kafka.common
import kafka.consumer

address = "http://192.168.10.4:8765/events.php"

kc = kafka.client.KafkaClient("192.168.10.4:9092")
consumer = kafka.consumer.SimpleConsumer(kc,
                                         "Foo",
                                         "stream-notifications",
                                         auto_commit=True)

for message in consumer:
    print message
    continue

    body = {'VM Create time': '{}'.format(t),
            'units': 'ms'}
    headers = {'content-type': 'application/json'}

    try:
        requests.post(url=address,
                      data=json.dumps(body),
                      headers=headers)
    except Exception as e:
        print("unable to post")
