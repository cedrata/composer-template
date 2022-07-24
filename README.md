# Authorized containerized MongoDB
This is an example of how to dockerize and secure a mongo db instance.

**Before doing anything make sure docker is installed!**

# Required steps
Create in this directory a new directory ```data/db``` before doing anything else if you wanto to store locally your data.

Introduce then the following environement variables in your system: 
- MONGO_INITDB_ROOT_USERNAME
- MONGO_INITDB_ROOT_PASSWORD
- MONGO_INITDB_DATABASE

Execute then the folloing command ```docker-compose --env-file .env up --build```, or ```docker compose up --build``` if you want to keep the env inside ```docker-compose.yml``` file. The informations contained in this .env file are necessary to startup the mongo container as a container requiring auth to access.

To run in detatched mode add the ```-d``` flag.

# Important notes
This example use a ```.env``` file to inject the environement variables into the container, which is not safe for production. This is for testing purposes only.