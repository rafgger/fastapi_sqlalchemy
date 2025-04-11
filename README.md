# Build a CRUD App with FastAPI and SQLAlchemy
# backend
have docker open
use bash:

activate virtual env: venv\Scripts\activate.bat

install all missing packages

uvicorn app.main:app --reload

open on: http://127.0.0.1:8000/docs

docker: docker-compose up -d

docker-compose down -v --remove-orphans
docker-compose up --build


(frontend: frontend-reactjs-crud-crypto-app  https://github.com/rafgger/frontend-reactjs-crud-crypto-app)

In this article, I'll provide you with a simple and straightforward guide on how you can build a CRUD app with FastAPI and SQLAlchemy. The FastAPI app will run on a Starlette web server, use Pydantic for data validation, and store data in an SQLite database.

![Build a CRUD App with FastAPI and SQLAlchemy](https://codevoweb.com/wp-content/uploads/2022/11/Build-a-CRUD-App-with-FastAPI-and-SQLAlchemy.png)

## Topics Covered

- Run the SQLAlchemy FastAPI App Locally
- Run the Frontend App Locally
- Setup FastAPI and Run the HTTP Server
- Designing the CRUD API
- Setup SQLAlchemy with SQLite
- Setup SQLAlchemy with PostgreSQL
- Create Database Model with SQLAlchemy
    - Database Model for SQLite Database
    - Database Model for Postgres Database
- Create Validation Schemas with Pydantic
- Define the Path Operation Functions
    - Get All Records
    - Create a Record
    - Update a Record
    - Retrieve a Single Record
    - Delete a Single Record
- Connect the API Router to the App

Read the entire article here: [https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy](https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy)

