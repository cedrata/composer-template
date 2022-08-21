# Authorized containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.

**Before doing anything make sure docker is installed!**

# Required steps
Create in this directory a new directory ```data/db``` before doing anything else.

Execute then the folloing command ```docker-compose --env-file .env up --build```, or ```docker compose up --build``` if you want to keep the env inside ```docker-compose.yml``` file. The informations contained in this .env file are necessary to startup the mongo container as a container requiring auth to access.

To run in detatched mode add the ```-d``` flag.