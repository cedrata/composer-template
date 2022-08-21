# Authorized containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.

**Before doing anything make sure docker is installed!**

# Required steps
Type in your shell ```$ cp .env.example .env``` and then update the environement variables in it.

The following variables are the variables to initialize the mongo container as you can see [here](https://hub.docker.com/_/mongo/)
- MONGO_INITDB_ROOT_USERNAME
- MONGO_INITDB_ROOT_PASSWORD
- MONGO_INITDB_DATABASE

The following variables are for the database administrator, which is required for an API to make updates.

If you want you could eventually add other readonly users to prevent unwanted updates.

Execute then the folloing command ```docker-compose --env-file .env up --build```, or ```docker compose up --build``` if you want to keep the env inside ```docker-compose.yml``` file. The informations contained in this .env file are necessary to startup the mongo container as a container requiring auth to access.

To run in detatched mode add the ```-d``` flag.