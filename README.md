# BookIt API

A production-ready REST API for a simple bookings platform called BookIt.

## Architectural Decisions

For this project, I chose **PostgreSQL** as the database. The relational nature of the data (Users, Services, Bookings, Reviews) makes a relational database a good fit. PostgreSQL's features like data integrity, robust data types, and concurrency support are well-suited for a transactional platform like this.

The application is built with **FastAPI**, a modern, fast (high-performance) web framework for building APIs.


**Alembic** is used for database migrations, allowing for version control of the database schema.

## How to Run Locally


1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/JoseAyobami/book>
    cd book
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Create a `.env` file.
    *   Fill in the required values in the `.env` file (see Environment Variables section).

5.  **Run database migrations:**
    ```bash
    alembic upgrade head
    ```

6.  **Start the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

#  Note
```
For the admin, i created an endpoint to create an admin user 
```

## Environment Variables

-   `DATABASE_URL`: The connection string for the PostgreSQL database.
-   `SECRET_KEY`: A secret key for signing JWTs.
-   `ALGORITHM`: The algorithm used for JWT encoding.
-   `ACCESS_TOKEN_EXPIRE_MINUTES`: The lifetime of an access token in minutes.
-   `REFRESH_TOKEN_EXPIRE_DAYS`: The lifetime of a refresh token in days.
-   `POSTGRES_USER`: The username for the PostgreSQL database.
-   `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
-   `POSTGRES_DB`: The name of the PostgreSQL database.



# Deployment Notes



## Deploying on Render

You can manually set up the service:

1.  **Create a new Web Service on Render.**
2.  **Connect your Git repository.**
3.  **Set the following environment variables in the Render dashboard:**
    *   `DATABASE_URL`: The connection string for the PostgreSQL database (you can use Render's own PostgreSQL service).
    *   `SECRET_KEY`: A secret key for signing JWTs.
    *   `ALGORITHM`: The algorithm used for JWT encoding.
    *   `ACCESS_TOKEN_EXPIRE_MINUTES`: The lifetime of an access token in minutes.
    *   `REFRESH_TOKEN_EXPIRE_DAYS`: The lifetime of a refresh token in days.
4.  **Set the start command to:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```
5.   **Deploy the service.**
