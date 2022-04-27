from src.db.relational_repository import RelationalRepository
from src.domain.metadata import Metadata
from src.db.oracle_queries import CREATE_TABLE_METADATA, CREATE_TABLE_SMT, CREATE_SEQUENCE_METADATA, METADATA_TRIGGER, \
    CREATE_SEQUENCE_SMT, SMT_TRIGGER
from deployment_utils.oracle_db import OracleDB
import logging
import cx_Oracle
import datetime

from src.config_reader import config
from src.domain.smt_entry import SmtEntry


class OracleRepository(RelationalRepository):
    def __init__(self):
        self._establish_connection()
        self._create_schema()

    def _establish_connection(self):
        self.connection = None
        try:
            self.connection = cx_Oracle.connect(
                config['oracle']['username'],
                config['oracle']['password'],
                config['oracle']['dsn'],
                encoding=config['oracle']['encoding'])
        except cx_Oracle.Error as error:
            logging.error(error)

    def __del__(self):
        self._close_connection()

    def _close_connection(self):
        if self.connection:
            self.connection.close()

    @OracleDB.drop_table_if_on_dev_env(component_names=['Metadata', 'SMT'])
    @OracleDB.drop_sequence_if_on_dev_env(component_names=['METADATA_IDENTITY', 'SMT_IDENTITY'])
    @OracleDB.drop_trigger_if_on_dev_env(component_names=['METADATA_TRIGGER', 'SMT_TRIGGER'])
    def _create_schema(self):
        """
        sqlcode: ORA-00955: name is already being used by existing object
        The error with this code is caught when the component being created with
        the specified name already exists in the database.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                begin
                    begin
                        execute immediate '{CREATE_SEQUENCE_METADATA}';
                        exception when others then
                          if sqlcode <> -955 then
                            raise;
                          end if;
                    end;
                    begin
                        execute immediate '{CREATE_SEQUENCE_SMT}';
                        exception when others then
                          if sqlcode <> -955 then
                            raise;
                          end if;
                    end;
                    begin
                        execute immediate '{CREATE_TABLE_METADATA}';
                        exception when others then
                          if sqlcode <> -955 then
                            raise;
                          end if;
                    end;
                    begin
                        execute immediate '{CREATE_TABLE_SMT}';
                        exception when others then
                          if sqlcode <> -955 then
                            raise;
                          end if;
                    end;
                    begin
                        execute immediate '{METADATA_TRIGGER}';
                        exception when others then
                          if sqlcode <> -4081 then
                            raise;
                          end if;
                    end;
                    begin
                        execute immediate '{SMT_TRIGGER}';
                        exception when others then
                          if sqlcode <> -4081 then
                            raise;
                          end if;
                    end;
                commit;
                end;""")

    def insert_metadata_row(self, metadata: Metadata):
        logging.info(f"Saving metadata: {metadata}")
        stmt = (
            "insert into metadata(time_of_event,in_out,car_body_id,car_body_type,voltage_program_type,skid_id,pendulum_id) values("
            ":time_of_event, "
            ":in_out,"
            ":car_body_id, "
            ":car_body_type, "
            ":voltage_program_type, "
            ":skid_id, "
            ":pendulum_id)")

        with self.connection.cursor() as cursor:
            cursor.execute(stmt, [
                datetime.datetime.strptime(metadata.time_of_event, "%Y-%m-%d %H:%M:%S.%f"),
                metadata.in_out,
                metadata.car_body_id,
                metadata.car_body_type,
                metadata.voltage_program_type,
                metadata.skid_id,
                metadata.pendulum_id
            ])
            self.connection.commit()

    def insert_smt_entry(self, smt_entry: SmtEntry):
        logging.info("Saving SMT entry.")
        stmt = ("insert into SMT(timestamp, skid_id, type_of_smt_event) values("
                ":timestamp,"
                ":skid_id,"
                ":type_of_smt_event"
                ")")

        with self.connection.cursor() as cursor:
            cursor.execute(stmt, [
                datetime.datetime.strptime(smt_entry.timestamp, "%Y-%m-%d %H:%M:%S.%f"),
                smt_entry.skid_id,
                smt_entry.type_of_smt_event
            ])
            self.connection.commit()
