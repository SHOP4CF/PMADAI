from src.consumers.basic_consumer import BasicConsumer


class PreprocessingResultConsumer(BasicConsumer):
    def __init__(self, topic_name):
        super().__init__(topic_name)

    def consume(self):
        for message in self.consumer:
            yield message
