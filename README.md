# Authorized containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.
The purpose of this repository is to provide a database for [this api](https://github.com/cedrata/fastapi-auth-template). The final objective is to create a docker compose file in [this other repository](https://github.com/cedrata/composer-template) to be able to launch the DB and the complete application example API+DB as a containerized application.

**Before doing anything make sure docker is installed!**

# Required steps
Create in this directory a new directory ```data/db``` before doing anything else.

Execute then the folloing command ```docker-compose --env-file .env up --build```, or ```docker compose up --build``` if you want to keep the env inside ```docker-compose.yml``` file. The informations contained in this .env file are necessary to startup the mongo container as a container requiring auth to access.

To run in detatched mode add the ```-d``` flag.