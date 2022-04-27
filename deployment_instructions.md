# To run in production (production mode):
1) Set up an Oracle instance in version 19.0.3  
2) Optionally (*tables will create automatically by build-in script, but if you prefer to have double confirmation about existence of tables, created them by hand*) create 4 tables and 1 sequence (optionally a new user and password):
```
CREATE SEQUENCE METADATA_IDENTITY
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE;

CREATE TABLE Metadata (
    id NUMBER NOT NULL,
    time_of_event TIMESTAMP NOT NULL,
    in_out VARCHAR2(10) NOT NULL,
    car_body_id VARCHAR2(20) NOT NULL,
    car_body_type VARCHAR2(10) NOT NULL,
    voltage_program_type VARCHAR2(10) NOT NULL,
    skid_id NUMBER NOT NULL,
    pendulum_id NUMBER NOT NULL,
    CONSTRAINT metadata_pk PRIMARY KEY (id)
);

CREATE TRIGGER METADATA_TRIGGER
BEFORE INSERT ON Metadata
FOR EACH ROW
BEGIN
   :NEW.id := METADATA_IDENTITY.NextVal;
END;

CREATE SEQUENCE SMT_IDENTITY
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE;

CREATE TABLE SMT (
    id NUMBER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    skid_id NUMBER NOT NULL,
    type_of_smt_event VARCHAR2(10) NOT NULL,
    CONSTRAINT smt_id PRIMARY KEY (id)
);

CREATE TRIGGER SMT_TRIGGER
BEFORE INSERT ON SMT
FOR EACH ROW
BEGIN
   :NEW.id := SMT_IDENTITY.NextVal;
END;

CREATE SEQUENCE PAINTING_IDENTITY
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE;

CREATE TABLE PaintingPredictions (
    id NUMBER NOT NULL,
    prediction_result BLOB NOT NULL,
    human_result BLOB NOT NULL,
    problematic_painting NUMBER(3) NOT NULL,
    preprocessing_status VARCHAR2(20) NOT NULL,
    time_of_event TIMESTAMP NOT NULL,
    in_out VARCHAR2(10) NOT NULL,
    car_body_id VARCHAR2(20) NOT NULL,
    car_body_type VARCHAR2(10) NOT NULL,
    voltage_program_type VARCHAR2(10) NOT NULL,
    skid_id NUMBER NOT NULL,
    pendulum_id NUMBER NOT NULL,
    features BLOB NOT NULL,
    raw_data BLOB NOT NULL,
    human_verified 	NUMBER(3) NOT NULL,
    date_modified TIMESTAMP NOT NULL,
    CONSTRAINT painting_predictions_pk PRIMARY KEY (id)
);

CREATE TRIGGER PaintingPredictionsTrigger
BEFORE INSERT ON PaintingPredictions
FOR EACH ROW
BEGIN
   :NEW.id := PAINTING_IDENTITY.NextVal;
END;

CREATE SEQUENCE ALERT_IDENTITY
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE;

CREATE TABLE ALERTS (
    id NUMBER NOT NULL,
    full_alert BLOB NOT NULL,
    category VARCHAR2(40) NOT NULL,
    sub_category VARCHAR2(40) NOT NULL,
    human_verified VARCHAR2(5) NOT NULL,
    alert_source VARCHAR2(100) NOT NULL,
    source VARCHAR2(20) NOT NULL,
    time_of_event TIMESTAMP NOT NULL,
    CONSTRAINT alert_id PRIMARY KEY (id)
);

CREATE TRIGGER ALERTS_TRIGGER
BEFORE INSERT ON ALERTS
FOR EACH ROW
BEGIN
   :NEW.id := ALERT_IDENTITY.NextVal;
END;

CREATE SEQUENCE ALERT_ID
     START WITH 1
     INCREMENT BY 1
     NOCACHE
     NOCYCLE;
```

3) Set up InfluxDb in version 2.x and create a user, an organization, bucket and authentication token for the PMADAI component.
4) Download kafka-docker submodule or run: `git clone https://github.com/wurstmeister/kafka-docker.git`
5) Create `.env` file which contains environmental variables needed to run the app (you may use .env.prod file as a template), 
   then set all the environmental variables accordingly to your environment (pay special attention to the "DEPLOYMENT_ENV" field - 
   in the production environment, be sure to set the flag as "PRODUCTION").
6) Run:
```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```

Remarks:
Right now the docker-compose.prod.yml file is prepared to run the development version and assumes 
that there exists an external docker network called `pmadai_default`. Oracle container is attached to this network. 
Furthermore, all docker images are building from the directories mentioned in the docker-compose.prod.yml file.

### To run in the development mode (not recommended in production)
First checkout the `develop` branch: `git checkout develop`

1) Run Oracle 19.0.3
2) Run InfluxDb 2.x
3) Prepare .env file accordingly to your environment. Within that file, set the `DEVELOPMENT_ENV` variable equal to "DEVELOP" 
   (*make sure you are convinced that you need to run this mode - it will delete tables from the database and recreate them!*)
4) If you want to use simulation data, make sure the `simulation_data.zip` file exists in the module orion-load-simulator, otherwise delete it and provide yours own data.
5) Download kafka-docker submodule or run: `git clone https://github.com/wurstmeister/kafka-docker.git`
6) Then run:
```
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up
```

The app should start at port 8080, see: http://localhost:8080. You can use a test account to log in: user->test, password->test
