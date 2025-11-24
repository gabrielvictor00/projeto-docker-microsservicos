FROM postgres:15-alpine

ENV POSTGRES_DB=desafio2_db
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=senha123

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432


