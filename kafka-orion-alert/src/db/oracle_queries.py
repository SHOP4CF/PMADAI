CREATE_SEQUENCE_ALERTS = """
CREATE SEQUENCE ALERT_IDENTITY
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE
"""

CREATE_TABLE_ALERTS = """CREATE TABLE ALERTS (
    id NUMBER NOT NULL,
    full_alert BLOB NOT NULL,
    category VARCHAR2(40) NOT NULL,
    sub_category VARCHAR2(40) NOT NULL,
    human_verified VARCHAR2(5) NOT NULL,
    alert_source VARCHAR2(100) NOT NULL,
    source VARCHAR2(20) NOT NULL,
    time_of_event TIMESTAMP NOT NULL,
    CONSTRAINT alert_id PRIMARY KEY (id)
)"""

ALERTS_TRIGGER = """
CREATE TRIGGER ALERTS_TRIGGER
BEFORE INSERT ON ALERTS
FOR EACH ROW
BEGIN
   :NEW.id := ALERT_IDENTITY.NextVal;
END;
"""

CREATE_SEQUENCE_ALERT_ID = """
CREATE SEQUENCE ALERT_ID
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE
"""