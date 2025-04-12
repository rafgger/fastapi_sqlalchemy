# Crypto CRUD App with FastAPI and SQLAlchemy
# backend

create your .env file + get API KEY from coingecko

docker-compose up -d

open on: http://localhost:8000/docs

use together with [my frontend ](https://github.com/rafgger/fastapi-frontend)

close with: docker-compose down

<img src="https://github.com/user-attachments/assets/620df06c-8e77-46f9-9813-552d6d652997" alt="frontend with docker" width="500"/>

<img src="https://github.com/rafgger/fastapi_sqlalchemy/blob/87789ea7f532d1815c4336feaccb9e59d578f8dd/env_variables.PNG" alt=".env file" width="500"/>


## local deployment 
use branch: run-localhost
have docker open

use bash:
activate virtual env: venv\Scripts\activate.bat

install all missing packages (pip install ###)

uvicorn app.main:app --reload

open on: http://localhost:8000/docs

(http://127.0.0.1:8000/docs)

docker: docker-compose up -d


(frontend: frontend-reactjs-crud-crypto-app  https://github.com/rafgger/frontend-reactjs-crud-crypto-app)

In this article, I'll provide you with a simple and straightforward guide on how you can build a CRUD app with FastAPI and SQLAlchemy. The FastAPI app will run on a Starlette web server, use Pydantic for data validation, and store data in an SQLite database.

<img src="https://github.com/user-attachments/assets/cd35d715-0fe0-45c3-851e-ee851986b1c1" alt="docker" width="300"/>


Starting template kindly provided by: 
[Github: Django_Crud_Project ](https://github.com/wpcodevo/Django_Crud_Project/tree/master) in [https://codevoweb.com/build-a-reactjs-crud-app-using-a-restful-api/](https://codevoweb.com/build-a-reactjs-crud-app-using-a-restful-api/) 

<img src="https://codevoweb.com/wp-content/uploads/2022/11/Build-a-CRUD-App-with-FastAPI-and-SQLAlchemy.png" alt="Build a CRUD App with FastAPI and SQLAlchemy" width="300"/>
    - Delete a Single Record
- Connect the API Router to the App

Read the entire article here: [https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy](https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy)

