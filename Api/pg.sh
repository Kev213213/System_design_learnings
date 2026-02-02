# postgres docker image

docker run --name my_postgres -d -e POSTGRES_PASSWORD=admin -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres


fastapi dev --reload app/main.py

# dummy table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(20) NOT NULL,
    content VARCHAR(200),
    published BOOLEAN NOT NULL DEFAULT FALSE,
    rating INTEGER
);
INSERT INTO posts (title, content, published, rating)
VALUES ('First Post', 'Hello from FastAPI + Postgres', true, 5);
