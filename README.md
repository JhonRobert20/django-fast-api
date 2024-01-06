# Real state backend

## Requirements

 * Docker
 * Docker Compose
 * [Python 3](https://www.python.org/)
 * [pre-commit](https://pre-commit.com/)

## About
Welcome to the Real state backend project!
- In this project I want to show you how to build a backend for a real state website.
- The backend is built with Django and Fast api - container web.
- The database is PostgreSQL and MongoDB.
- The views contain login, logout, register and a list of estates.
- The API contains endpoints for the estates.
- There is a command to populate the database with fake data.
- The most interesting part of this project is how the django app is communicated with the fast api app.
- Please read all the documentation to understand how to use the project.
- Please, check the TODO section to see what I would like to improve in the future.

## Important
- Use localhost:8000, not 0.0.0.0

## Setup

Install the git hooks with:

```bash
pre-commit install
cp ./git-hook-commit-msg .git/hooks/commit-msg
```

Run the `install.sh` script:

```bash
./install.sh
```

Start Docker containers:

```bash
docker-compose up -d
```

Create a new superuser:

```bash
$ docker-compose run web python manage.py createsuperuser
```

Link to http://localhost:8000/web/admin/ and log in!



## Access Adminer in the browser

To access the database, go to http://localhost:8080/ and use the following credentials:

 * System: PostgreSQL
 * Server: database
 * Username: real_state
 * Password: real_state!
 * Database: real_state


## Access Mongo Express in the browser

To access the database, go to http://localhost:8081/ and use the following credentials:

 * Username: real_state
 * Password: real_state!


## Access to the API

To access the API, go to http://localhost:8000/api/docs/


## Access to django admin

To access the API, go to http://localhost:8000/web/admin/


## Populate the database

To populate the database, run the following command:

```bash
docker-compose run web python manage.py populate
```

## Run tests

```bash
docker-compose run web pytest
```

## TODO
- Recover password view
- Convert the estate before saving it to the database
- Add download csv endpoint
- Add download csv action in the admin panel
- Add JWT authentication for the API
