from uuid import uuid4
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.schema_registry_client import Schema
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

from django.conf import settings
from django.http import HttpResponse

from .constants import USER_SCHEMA, USER_TOPIC
from .transformers import user_to_dict
from .models import UserProducer

schema_registry_conf = {'url': 'http://172.168.1.1:8085'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
schema = Schema(schema_str=USER_SCHEMA, schema_type='JSON')
schema_registry_client.register_schema(subject_name="user", schema=schema)


def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


json_serializer = JSONSerializer(USER_SCHEMA, schema_registry_client, user_to_dict)

producer_conf = {'bootstrap.servers': '172.168.1.1:29092',
                 'key.serializer': StringSerializer('utf_8'),
                 'value.serializer': json_serializer}
producer = SerializingProducer(producer_conf)


def send(request, username, data, token):
    user = UserProducer(username=username,
                        data=data,
                        token=token)

    producer.produce(topic=USER_TOPIC, key=str(uuid4()), value=user,
                     on_delivery=delivery_report)
    producer.flush(30)
    return HttpResponse(status=200)
