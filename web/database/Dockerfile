FROM postgres:latest

ENV POSTGRES_DB=realestateDB
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin

# Create schema and tables
COPY ./schema.sql /docker-entrypoint-initdb.d/
COPY ./misc.sql /docker-entrypoint-initdb.d/