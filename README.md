# Webtronics FastAPI app

The application is implemented:

- Form of authentication (JWT) and registration
- Ability to register and log in
- Ability to create, edit, delete and view messages
- The user can like or dislike other users’ posts, but not his own 
- User Interface Documentation (Swagger/ReDoc)
- Getting additional information about users using https://clearbit.com/platform/enrichment
- Verification of an email address using hunter.co
- Docker (Dockerfile and docker-compose)

Stack: FastAPI, Tortoise ORM, PostgresSQL

## Install:

   - git@github.com:ieasycat/webtronics_task.git 
   - virtualenv -p python3 .venv
   - source venv_name/bin/activate
   - python -m pip install -r requirements.txt
   - Creation .env file. Example .env_example

## DataBase

1. Init DB
   - aerich init -h
2. Creating a config and migration(config.tortoise_config.AERICH_CONFIG file path) 
   - aerich init -t config.tortoise_config.AERICH_CONFIG
3. Create a migration
   - aerich init-db
4. When changing the table (deleting, deleting columns)
   - aerich migrate --name drop_column
5. Writing changes to the table
    - aerich upgrade


## Launching the application:

   - uvicorn app:app --reload

## Description of methods and documentation:

   - http://localhost:8000/docs/
   - http://localhost:8000/redoc

## Docker:

   - Creation .env_docker file. Example .env_docker_example
   - docker-compose up -d --build

## Technical task:

1. There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
2. As a user I need to be able to signup and login
3. As a user I need to be able to create, edit, delete and view posts
4. As a user I can like or dislike other users’ posts but not my own 
5. The API needs a UI Documentation (Swagger/ReDoc)


### Additional tasks:

1. Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup
2. Use emailhunter.co for verifying email existence on registration
3. Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added) 
