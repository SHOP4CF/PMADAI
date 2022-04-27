# PMADAI component

Predictive Maintenance and Anomaly Detection in Automotive Industry (PMADAI) component is being developed at Poznań Supercomputing and Networking Center in close collaboration with Volkswagen Poznań as a part of the [SHOP4CF project](https://www.shop4cf.eu/). The first objective of our component is detection of problems during the KTL painting process, which stands for cataphoretic dip coating of car bodyworks. The second objective is to support maintenance needs in the KTL area. Both objectives contribute to the main goal of our component, which is to support human workers during their day-to-day tasks within the factory.

The KTL process is applied in the Volkswagen paint shop to provide a layer of paint on the bodywork that will protect it against corrosion. The car bodyworks are immersed in a water-based, electrically conductive paint. Electrical field is then applied causing the paint to be deposited on the parts. It is crucial to ensure a uniform layer of coating even in hollow spaces and on sharp edges. However, there are many reasons which can cause difficulties during the painting process. For example, mechanical wear out of painting equipment may lead to problems with electrical conductivity.

The component collects production data from various sources and uses them to provide real-time predictions, alerts, and advanced analytics. All communication between our component and its working environment takes place through FIWARE. In order to provide reliable predictions, some of the recent advances in machine learning, and particularly anomaly detection, are applied. The analytical insights that users gain from the component help them early identify problems which may lead to damage of equipment in the KTL area, as well as to detect potential quality defects in car bodyworks. Ultimately all of this allows to reduce downtime and unnecessary maintenance procedures.

Our component provides a user interface, which allows to explore recent paintings in the KTL aggregate. The visualization of the painting process data provided by PMADAI is interactive and shows current waveforms associated with the painting as well as contextual metadata needed to carefully assess the situation. Any deviations from normal behavior are highlighted by the software.

## Development

More information regarding development of the PMADAI component and project structure may be found in the [documentation](./docs/development.md).

## Deployment

### Prerequisites

Need to have installed: git, docker, docker-compose

Oracle, Influx and Orion running.

### DEPLOYMENT_ENV

`DEPLOYMENT_ENV` - variable (in .env file) specifying the type of deployment.

- Develop - setting this value will **<u>clear the contents of the database</u>** when the project is started and **<u>allow</u>** the use of a test user.
- Production - setting this value will **<u>not</u>** wipe the database and will **<u>not</u>** allow you to use the test user.

### Starting the project

> If you are launching a project for the first time and you do not have the appropriate database components set up,
> go to the Oracle and InfluxDB points (below in the 'starting the project' section) which show how to set up these components.


#### First downloading from a remote repository:

```
git clone git@bitbucket.com:<project>/development.git <project> && cd <project>
git submodule init && git submodule update
cp .env.dev .env
```

#### To create a network for all involved containers

```
docker network create --driver bridge pmadai_default
```
Connect the container to some shared network for easy access from other containers:

#### Modules password
First, in files **.\backend\config.yml** and **.\processing\config.yml**, you should set a password in order to securely
transfer data between modules.

#### Oracle network

When using dockerized oracle:
```
docker network connect pmadai_default oracle19
```
or (depending on docker-compose.yml setup)
```
docker network connect docker_default oracle19
```

To test oracle connection:
```
docker exec -it pmadai_data_collection_1 /bin/bash
apt-get install telnet
telnet 192.168.1.107 1521
telnet 172.17.0.1 1521
```

#### InfluxDB network

Connecting InfluxDB to the same network
```
docker network connect pmadai_default influxdb
```
or (depending on `docker-compose.yml` setup)
```
docker network connect docker_default influxdb
```

#### Orion network
If orion is in different network than rest of components.
```
docker network connect pmadai_default orion_orion_1
```
where 'orion_orion_1' is name of orion - may by different

or (depending on docker-compose.yml setup)
```
docker network connect docker_default orion_orion_1
```

To test orion connection:
```
curl --location --request GET 'http://localhost:1026/version/'
```

#### docker-compose commands

To rebuild (after updating submodules):
```
docker-compose -f docker-compose.{dev,prod}.yml build
```

To run:
```
docker-compose -f docker-compose.{dev,prod}.yml up -d
```

To kill:
```
docker-compose -f docker-compose.{dev,prod}.yml down
```

To list:
```
docker-compose ps
```

### Oracle

#### Download and install Oracle

To build official docker image of Oracle Database 19.3.0, please visit the folliowing [repository with docker Images from Oracle](https://github.com/oracle/docker-images/tree/main/OracleDatabase/SingleInstance).

Download Oracle binaries (file should be named something like `LINUX.X64_193000_db_home.zip`),
put them into `dockerfiles/<version>` and run in via Git Basha:
```
sudo docker build -t oracle/database:19.3.0 --build-arg DB_EDITION=EE .
```

#### Run Oracle container

To run the container:
```
sudo docker run -d -it --rm --name oracle19 -e ORACLE_PWD='oracle' -p 1521:1521 -p 5500:5500 oracle/database:19.3.0
```

Check the logs (the container takes some time to start up)
```
sudo docker logs oracle19
```

Connect with sqlplus and create tables:
in terminal cmd/powershell type command:
```
set ORACLE_SID=oracle19
```

where oracle19 is your name of database (may be different)

### SQLplus

to open terminal directly with docker desktop app or by cmd/powershell with command:
```
docker exec -it --user=oracle oracle19 bash 
```

where oracle19 is your name of database


If you want to connect directly to the base and use sqlplus, type:
```
sqlplus system/oracle@//192.168.0.16:1521/ORCLCDB
```

where `192.168.1.107` replace with your own internal ip address

### Run Orion

This section is only required when *no* FIWARE orion instance is running, and the user needs access to the context-broker.

To rebuild (after updating submodules):
```
docker-compose -f docker-compose.orion.yml build
```

To run:
```
docker-compose -f docker-compose.orion.yml up -d
```

To kill:
```
docker-compose -f docker-compose.orion.yml down
```

### InfluxDB

#### Windows

```
https://portal.influxdata.com/downloads/
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.7-windows-amd64.zip -UseBasicParsing -OutFile influxdb2-2.0.7-windows-amd64.zip
Expand-Archive .\influxdb2-2.0.7-windows-amd64.zip -DestinationPath 'C:\Program Files\InfluxData\influxdb2\'
```

#### Linux

```
https://docs.influxdata.com/influxdb/v2.0/install/?t=Linux
```

#### Running preprocessing on recs

```
cd pmadai/preprocessing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="`pwd`"
python src/scripts/preprocess_batch.py
```

### (Windows) Troubleshooting with docker-compose build

In kafka-docker/docker-compose.yml replace lines:

```
kafka:
    build: .
```
to:

```
kafka:
    #build: .
    image: wurstmeister/kafka
```


type in cmd/Powershell:
```
set COMPOSE_CONVERT_WINDOWS_PATH=1
```


If still have problem, try pull whole repo with previously typed command in Git Bash:
```
git config --global core.autocrlf false
```

### (Windows) Troubleshooting with docker-compose up

Inside '.env' file:

- remove all occurrences of quote sign in all assignments to `INFLUX` like variables.
