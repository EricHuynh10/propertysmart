POSTGRES_VERSION=13.2

run:
	docker rm -f postgres || true
	docker run -p 5432:5432 -d --name=postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e PGDATA=/var/lib/postgresql/data/pgdata -v ${PWD}/data/db:/var/lib/postgresql/data postgres:${POSTGRES_VERSION}
