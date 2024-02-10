# How to install

```bash
pip install -r requirements.txt
```

# How to run

To start
1. Start the virtual environments
- realestate_env\Scripts\activate

1. Start database on docker
- docker start RePostgresContainer
- Port to access this container on local machine is 5433

2. Crawl data and import it to database
- navigate to adhoc-scripts folder
- run data_prep.py

3. Run backend
- Navigate to .\web\backend\
- Run the following:
    uvicorn .\web\backend\main:app --reload

4. Start frontend
- Run: npm start
- To build: run npm build



# Running front end Nginx server
docker build -t my-frontend-app .
docker run -d -p 8080:80 my-frontend-app

# Running database server
docker build -t re-postgres-image .\web\database
docker volume create realestateVol
docker stop RePostgresContainer
docker start RePostgresContainer
docker rm -v RePostgresContainer
docker run --name RePostgresContainer -e POSTGRES_PASSWORD=admin -p 5433:5432 -v realestateVol:/var/lib/postgresql/data -d re-postgres-image
docker exec -it RePostgresContainer psql -U admin realestateDB

