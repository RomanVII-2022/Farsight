# Product API

## How to Run The Project
> Ensure you have postgresql running locally
1. Clone the project
2. Create a virtual environment
   
           python -m venv virtual
   
4. Activate the virtual environment
   
           source virtual/bin/activate
   
6. Install all the required dependencies that are listed in the requirements.txt file.
   
           pip install -r requirements.txt
   
8. Run the project using the following command:

           python manage.py runserver

## Run Project Using Docker Compose
> I have dockerized the project.

1. Make migrations

            docker compose run myapp python manage.py migrate

2. Run docker compose

            docker compose up


## End Points
1. ^users/ - must be admin permissions
2. ^users/pk/ - must be admin permissions
3. ^products/ - must be authenticated or read only permissions
4. ^products/pk/ - must be owner of prduct or read only
5. login - basic authentication
6. logout - basic authentication
7. api/token/ - token authentication
8. api/token/refresh/ - token authentication. Refresh access token.
9. api/token/verify/ - verify if access token is still valid
