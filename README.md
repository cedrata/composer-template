# Composer template
This is a simple template for a docker compose application with a DB managed by a FastAPI API.
All of this exists as a personal documentation, to help me in the future to do similar things, I hope it can help someone else too. For this reason I decided that if you want to support me on the development of this repository and maybe future projects you can now donate with ko-fi just by clicking the following button.


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E5E3EKB)

Thank you to everyone that will decide to support this and other projects <3

# General informations
This project depends on two repositories that can be installed after cloning this one on your machine by simply following [those steps](https://www.w3docs.com/snippets/git/how-to-clone-including-submodules.html). After those steps are completed simply follow along with the following steps.

More precisely this repository depends on:
- [fastapi-auth-template v0.1.2](https://github.com/cedrata/fastapi-auth-template/releases/tag/0.1.2)
- [fastapi-auth-template-db v0.0.0](https://github.com/cedrata/fastapi-auth-template-db/releases/tag/0.0.0)

# Create the environment variables
To start this application some environement variables are required.
Simply follow the next steps to generate the two required files.

## fastapi-auth-template
For this step the ```./fastapi-auth-templtate/scripts/init.sh``` script will be used.

You can type ```$ ./fastapi-auth-templtate/scripts/init.sh $(pwd)/env/.api.env``` to generate the file and provide the required inputs:
- db username -> admin
- db password -> admin
- db host -> db (which is the db containers name)
- db port -> 27017
- db name -> fastapi-auth-template

The produced file will be something similar to this:
```
SECRET_KEY=super-secret-key-automatically-generated
CONFIGS_DIR=/app/configs
LOGGING_DIR=/app/logs
DB_USERNAME=admin
DB_PASSWORD=admin
DB_HOST=db
DB_PORT=27017
DB_NAME=fastapi-auth-template
```

As you can see there are two directories: configs and logging.
This have been set by default to ```/app/something-else``` because in the composer file the container volumes will be mounted in those directories.

## fastapi-auth-tempalte-db
For this step you can copy in the ```./env``` directory the ```./fastapi-auth-template-db/.env.example``` as ```.db.env```, if you prefer type in your shell ```$ cp ./fastapi-auth-template-db/.env.example ./env/.db.env```, the file can be copied without any changes.
If you want to change anything make sure to update the ```./env/.api.env``` file db variables.

# Start the containers
Now that the environment variables are created you can launch the containers with ```$ docker-compose up --build``` so the fastapi-auth-template image will be build and then the required containers will be generated.

To test everything's working just fine you can firs check the connection to the connecting to mongodb by typing the following connection string inside MongoDB compass ```mongodb://admin:admin@localhost:27017/fastapi-auth-template``` (here we are using the localhost becuase we provided ports in docker compose to map the mongodb instance container with our localhost). After you were able to connect check the api is working correctly by typeing ```$ curl http://localhost:8000/cdrt/``` in your shell and it should return an "Hello, world" like message. Alternatively to explore the available api you can type in your browser http://localhost:8000/docs, and it should return the swagger documentation

# Notes
Currenlty no networks in the docker-compose file are used, and to let the api container connect to the containerized db the api must have ```db``` as host, because is the db container name and it work as an host from container to container.
