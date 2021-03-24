from typing import Dict, Any

from confluent_kafka.avro import AvroProducer, AvroConsumer


class MockPublishResponse:

    @staticmethod
    def produce():
        return

    @staticmethod
    def flush():
        return


class MockMessage:
    def __init__(self, topic, value, partition=0):
        self.topic = topic
        self.value = value
        self.partition = partition

    def topic(self):
        return self.topic

    def value(self):
        return self.value

    def partition(self):
        return self.partition

    def error(sele):
        return False


class MockConsumeMessage:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def poll(self, timeout=1):
        return MockMessage(**self.kwargs)


def mock_kafka_publish(monkeypatch):
    """
    def test_publish_shop(monkeypatch):
        mock_kafka_publish(monkeypatch)
    """

    def mock_call(*args, **kwargs):
        return MockPublishResponse()

    monkeypatch.setattr(AvroProducer, "produce", mock_call)
    monkeypatch.setattr(AvroProducer, "flush", mock_call)


def mock_kafka_consume(
        monkeypatch,
        topic: str,
        value: Dict[str, Any],
        partition=0
):
    """
    :param topic: 消费的topic
    :param value: 消费的数据
    :param partition: 默认0

    def test_consume_info(monkeypatch):
        topic = "store-info-update-info"
        value = {
            "app_name": "chat",
            "sid": "123",
            "seller_nick": "123"
        }
        mock_kafka_consume(monkeypatch, topic, value)
    """

    def mock_call(mock_return_value):
        def mock(*args, **kwargs):
            return MockConsumeMessage(**mock_return_value)

        return mock

    return_value = {
        "topic": topic,
        "value": value,
        "partition": partition
    }
    monkeypatch.setattr(
        AvroConsumer, "poll", mock_call(return_value)
    )
