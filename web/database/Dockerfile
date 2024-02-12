FROM postgres:latest

ENV POSTGRES_DB=realestateDB
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin

# Create schema and tables
COPY ./01-schema.sql /docker-entrypoint-initdb.d/
COPY ./02-misc.sql /docker-entrypoint-initdb.d/