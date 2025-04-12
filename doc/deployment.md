# Deployment

## Initial Setup

Clone this project somewhere onto your server. This will most require
you to have `git` installed, but I guess you can alternatively just download a .zip
file of the repository and unpack it.

## Creating the Containers

Once you checked out the repository you need to create an `.env` file in the root folder.
The following variables are required:

* `POSTGRES_USER` - Username for the database
* `POSTGRES_PASSWORD` - Password for the database
* `POSTGRES_DB` - Name of the database that will be created
* `DISCORD_GUILD_ID` - The ID of the Discord server whose members will be shown on the front page
* `DATABASE_DRIVER` - This should be set to `postgresql`
* `DATABASE_HOST` - This should be set to `db`
* `DATABASE_PORT` - This should be set to `5432`
* `DATABASE_USER` - Needs to be the same as `POSTGRES_USER`
* `DATABASE_PASSWORD` - Needs to be the same as `POSTGRES_PASSWORD`
* `DATABASE_NAME` - Needs to be the same as `POSTGRES_DB`
* `JWT_SECRET_KEY` - A secret key for the JWT token; this should be a long random string
* `SAPHI_API_URL` - URL of the Saphi Leaderboard API where users are fetched from
* `SAPHI_API_TOKEN` - Token for the Saphi Leaderboard API

After creating the `.env` file, just run the `docker-compose.yml` in the root folder:

```bash
$ docker-compose up -f docker-compose.yml -p saphi-custom-tracks
```

The compose file will create 3 containers:

* The REST API container `saphi-custom-tracks-api`, running on port **5000**
* The web application container `saphi-custom-tracks-web`, running on port **3000**
* The database container `db`, running on port **5432**
* The adminer container `adminer`, running on port **8080**

All containers are running on the network interface `0.0.0.0`, that means all ports are accessible from the outside. Besides that,
there will be a folder created under `/root` that contains exposed directories of the database and the API. Those are:

* `/root/docker-data/api/resources` - Contains the uploaded files
* `/root/docker-data/db` - Contains the database files for backups

## Migrations

Once the docker compose has been booted up, the migrations need to be applied to bring the database to its current state.

```bash
$ docker exec -ti [container_id] flask --app api db upgrade
```

The `[container_id]` can be found by running `docker ps` and looking for the container with the name `saphi-custom-tracks-api`.

## Security

I recommend installing some reverse proxy in front of the api, frontend, adminer and the database
to handle SSL, request throttling and other things. None of the containers come preconfigured in a secure way
and the REST API even uses Flask's development webserver, which is not intended to be used for production.

Please secure the containers properly.
