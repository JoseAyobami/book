# BookIt API

A production-ready REST API for a simple bookings platform called BookIt.

## Architectural Decisions

### Database: PostgreSQL

I have chosen **PostgreSQL** for this project. Here's why:

*   **Relational Integrity:** The data model (Users, Services, Bookings, Reviews) is highly relational. A booking connects a user and a service, and a review is tied to a booking. PostgreSQL's enforcement of foreign key constraints and ACID compliance ensures data integrity at the database level, which is critical for a transactional system like this.
*   **Data Types and Constraints:** PostgreSQL offers a rich set of data types (like `TIMESTAMP WITH TIME ZONE`) and powerful constraint capabilities. This allows for robust data validation directly within the database, complementing the application-level validation done by Pydantic.
*   **Scalability and Concurrency:** PostgreSQL has excellent support for concurrent transactions, which is essential for a bookings platform where multiple users might try to book overlapping time slots. Its performance under load is well-established.
*   **Maturity and Tooling:** As a mature and widely-used database, PostgreSQL has a vast ecosystem of tools for administration, migration (like Alembic, which is a requirement), and performance analysis.

While MongoDB could work, its document-based nature is less ideal for this tightly-coupled, relational data, and would require implementing more data integrity logic at the application level.

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd bookit
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
    *   Copy the `.env.example` to a new `.env` file.
    *   Fill in the required values in the `.env` file (database URL, JWT secret, etc.).

5.  **Run database migrations (if using Alembic):**
    ```bash
    alembic upgrade head
    ```

6.  **Start the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Environment Variables

| Variable          | Description                               | Example                                                 |
| ----------------- | ----------------------------------------- | ------------------------------------------------------- |
| `DATABASE_URL`    | The connection string for the PostgreSQL database. | `postgresql://user:password@localhost/bookit`           |
| `SECRET_KEY`      | A secret key for signing JWTs.            | `your-very-secret-key`                                  |
| `ALGORITHM`       | The algorithm used for JWT encoding.      | `HS256`                                                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | The lifetime of an access token in minutes. | `30`                                                    |

## Deployment

**Production URL:** [To be added]
**API Docs URL:** [To be added]/docs
