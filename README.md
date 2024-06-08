# Real Estate Listing Application

Back-end side of a Real Estate Listing application, containing two main models and API endpoint groups:

- Users
- Listings

---

The implementations includes below features:

- Authentication route (/token/) can only be accessed 5 times a minute by an IP
- JWT Authentication (OAuth2)
- Logging all requests inside `logs.txt` file by the time and the ip of the request
- Each user can only be logged in on one device-only at a time (This is done using Redis)
- Fully dockerized (Dockerfile and docker-compose)
- Printing username for each successful login
- A counter counts each time the application is started inside `count.txt` file
- Database migrations implemented using `alembic`

---

The tech stack consists of:

- FastAPI
- PostgreSQL
- SQLAlchemy (fully asynchronous)
- Redis (for caching)
- Alembic (for migratrions)

---

The app is fully dockerized, just run `docker-compose up`, and you are good to go on `localhost:8000`

NOTE: You must specify below environment variables inside a `.env` in a folder named `docker-env`:

- JWT_SECRET
- JWT_ALGORITHM
- JWT_EXPIRY_TIME_IN_SECONDS
- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- REDIS_HOST
- REDIS_PORT
- REDIS_DB
- SUPERUSER_USERNAME
- SUPERUSER_PASSWORD
- SUPERUSER_EMAIL
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- PGADMIN_DEFAULT_EMAIL
- PGADMIN_DEFAULT_PASSWORD
