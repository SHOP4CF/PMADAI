# Set base image (host OS)
FROM python:3.8

# This microservice has the context of the entire project in order to be able to access deployment_utils and avoid using docker volume.
COPY data_collection/config.yml .

# Setup oracle instantclient libraries
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y libaio1 wget unzip \
            && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
            && unzip instantclient-basiclite-linuxx64.zip \
            && rm -f instantclient-basiclite-linuxx64.zip \
            && cd /opt/oracle/instantclient* \
            && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
            && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
            && ldconfig

# Copy the dependencies file to the working directory
COPY /data_collection/requirements.txt /data_collection/

# Install dependencies
RUN pip install -r /data_collection/requirements.txt

WORKDIR /data_collection/src

# Copy the content of the local src directory to the working directory
COPY /data_collection/src/ .

WORKDIR ../

COPY deployment_utils/ /data_collection/deployment_utils/

# Set pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/"

# Command to run on container start
CMD python src/main.py