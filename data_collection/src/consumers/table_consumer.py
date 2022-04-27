import cx_Oracle

from src.consumers.basic_consumer import BasicConsumer
import logging

from src.db.oracle_repository import OracleRepository
from src.db.relational_repository import RelationalRepository
from src.domain.metadata import Metadata
from src.domain.smt_entry import SmtEntry


class TableConsumer(BasicConsumer):
    def __init__(self, topic_name):
        super().__init__(topic_name)
        self.repository: RelationalRepository = OracleRepository()

    def consume(self):
        for message in self.consumer:
            logging.info(f"{self.topic_name}: writing {message.value}")
            if self.topic_name == "Metadata":
                try:
                    metadata = Metadata(metadata_json_dict=message.value)
                    self.repository.insert_metadata_row(metadata)
                except TypeError as te:
                    logging.error(f"Could not construct Metadata object from message: {message}. Error: {te}")
                except cx_Oracle.DatabaseError as err:
                    logging.error(f"Could not store Metadata in database: {err}")

            elif self.topic_name == "SMT":
                try:
                    smt_entry = SmtEntry(smt_entry_json_dict=message.value)
                    self.repository.insert_smt_entry(smt_entry)
                except TypeError as te:
                    logging.error(f"Could not construct and save SMT Entry object from message: {message}. Error: {te}")
                except cx_Oracle.DatabaseError as err:
                    logging.error(f"Could not store SMT Entry in database: {err}")