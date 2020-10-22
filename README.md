# THORIUM - BACK-END SERVICES
WEB_BACKEND provides infrastructure for communication between users(front-end application) 
and hardware (THORIUM systems).

## Conventions
In this document you will find a number of text styles / syntax elements that distinguish 
between information types.

The following element describes an action that user should run on their own system:

    ps -auxw | grep "*.txt"

If you find any element in <> brackets that means that it is left to user to insert some value 
instead of those brackets. For example:

    mkdir <your_directory_name>

means:

    mkdir some_dir_name

## Requirements
Necessary software for this project: postgresql, redis, python3.7.
To install the software on Debian based systems do the following.

    sudo apt update
    sudo apt dist-upgrade
    sudo apt install python3.7 python3.7-dev  postgresql postgresql-common\
    postgresql-10-postgis-2.4 postgresql-10-postgis-2.4-scripts\
    postgresql-10-postgis-scripts postgresql-contrib postgresql-plpython3-10\
    postgis lua-redis redis redis-redisearch redis-sentinel redis-server redis-tools\
    automake git-flow

## Postgresql configuration
To configure postgresql on Debian based systems follow these instructions:
[How To Install and Use PostgreSQL on Ubuntu 18.04 \| DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

    CREATE DATABASE <db_name_from_config_file>;
    CREATE USER <user_name_from_config_file> with encrypted password <'password_from_config_file'>;
    GRANT ALL PRIVILEGES ON DATABASE <db_name_from_config_file> TO <user_name_from_config_file>;
    CREATE EXTENSION postgis;
    CREATE EXTENSION postgis_topology;

## Get the latest code

Clone the repository:
    
    git clone git@gl.nv-labs.com:nv-labs/thorium/web_backend.git

The project is using git-flow branching model. To use the latest code switch to develop branch

    git checkout origin/develop develop

And pull the latest code.

## Install virtual environment requirements
Project is using python3.7 as a default(necessary because of async functionalities).
To isolate project requirements from system we are using virtual environments.
The point of v
To create virtual environment for development purposes install virtualenvwrapper:

    On debian based systems:
    sudo apt install virtualenvwrapper

Default virtual env directory (directory used to store virtual environments) is placed in
user home directory:

    ~/.virtualenvs

To create new virtual env do the following:

    mkvirtualenv -p /usr/bin/python3.7m <local_env_name>
 

## Setup local environment
To enter virtual environment run the following code:

    workon <local_en_name>

Go to the directory where you pulled git repo, and add it to python path:

    add2virtualenv .

After you added project to python path it is necessary to install all dependencies for project.

    cd web_backend
    pip install -U -r requirements.txt


## Create database and populate initial data
To configure project and properly set it up it is necessary to create the database and populate it 
with initial data. To populate database and create db project tables run the following commands:
    
    cd migrations

If the versions directory does not exist create it:

    mkdir versions
    
To create tables necessary for the project run the following commands:

    alembic revision --autogenerate -m "Initial load."
    alembic upgrade head
    
To populate the data for testing fun the following commands:

    cd data_loader
    python user_load.py
    python permission_matrix.py

## Running the server locally
To run a server locally you just need to run run.py

    python run.py

## Run app via gunicorn
To run a server on test environment or production run the app via the gunicorn.

     gunicorn --bind 127.0.0.1:8081 --workers 16 --threads 8 --worker-class sanic.worker.GunicornWorker thorium:app


## Run app via uvicorn
To run a server on test environment or production run the app via the uvicorn.
uvicorn --workers 8 --uds /tmp/uvicorn-test.sock --http h11 --host 127.0.0.1 --port 8000 run:app
