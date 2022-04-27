from src.db.relational_repository import RelationalRepository
from src.db.oracle_queries import CREATE_TABLE_ALERTS, CREATE_SEQUENCE_ALERT_ID, ALERTS_TRIGGER, CREATE_SEQUENCE_ALERTS
from src.handlers.alerts_handler import Alert
from src.config_reader import config
from deployment_utils.oracle_db import OracleDB
import logging
import cx_Oracle
import datetime
import json


class OracleRepository(RelationalRepository):
    def __init__(self):
        self._establish_connection()

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

    @OracleDB.drop_table_if_on_dev_env(component_names=['ALERTS'])
    @OracleDB.drop_sequence_if_on_dev_env(component_names=['ALERT_ID', 'ALERT_IDENTITY'])
    @OracleDB.drop_trigger_if_on_dev_env(component_names=['ALERTS_TRIGGER'])
    def create_schema(self):
        """
        sqlcode: ORA-00955: name is already being used by existing object
        The error with this code is caught when the component being created with
        the specified name already exists in the database.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                            begin
                                begin
                                    execute immediate '{CREATE_SEQUENCE_ALERTS}';
                                    exception when others then
                                      if sqlcode <> -955 then
                                        raise;
                                      end if;
                                end;
                                begin
                                    execute immediate '{CREATE_TABLE_ALERTS}';
                                    exception when others then
                                      if sqlcode <> -955 then
                                        raise;
                                      end if;
                                end;
                                begin
                                    execute immediate '{ALERTS_TRIGGER}';
                                    exception when others then
                                      if sqlcode <> -4081 then
                                        raise;
                                      end if;
                                end;
                                begin
                                    execute immediate '{CREATE_SEQUENCE_ALERT_ID}';
                                    exception when others then
                                      if sqlcode <> -955 then
                                        raise;
                                      end if;
                                end;
                            commit;
                            end;""")

    def get_unique_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute("select ALERT_ID.nextval from dual")
            unique_id, = cursor.fetchone()

        logging.debug(unique_id)
        return int(unique_id)

    def insert_alert(self, alert: Alert):
        logging.info("Saving Alert to database.")

        database_statement = ("insert into ALERTS(id, full_alert,"
                              "category,"
                              "sub_category,"
                              "human_verified,"
                              "alert_source,"
                              "source,"
                              "time_of_event) values("
                              ":id,"
                              ":full_alert,"
                              ":category,"
                              ":sub_category,"
                              ":human_verified,"
                              ":alert_source,"
                              ":source,"
                              ":time_of_event"
                              ")")

        orion_body_blob = str.encode(json.dumps(alert.orion_body))
        time_of_event = datetime.datetime.strptime(alert.date_issued, alert.datetime_format)

        logging.debug(f'Inserted alert: {alert}')

        with self.connection.cursor() as cursor:
            cursor.execute(database_statement, [alert.id,
                                                orion_body_blob,
                                                alert.category,
                                                alert.sub_category,
                                                alert.human_verified,
                                                alert.alert_source,
                                                alert.source,
                                                time_of_event])
            self.connection.commit()
