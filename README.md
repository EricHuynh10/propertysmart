# How to install

```bash
pip install -r requirements.txt
```

# How to run

1. Start the virtual environments
```cmd
realestate_env\Scripts\activate
```

2. Start database on docker
- docker start RePostgresContainer
- Port to access this container on local machine is 5433

3. Crawl data and import it to database
- navigate to adhoc-scripts folder
- run data_prep.py

4. Run backend
- Navigate to .\web\backend\
- Run the following:
    uvicorn .\web\backend\main:app --reload

5. Start frontend
- Run: npm start
- To build: run npm build



# Running front end Nginx server
docker build -t my-frontend-app .
docker run -d -p 8080:80 my-frontend-app

# Running database server
docker build -t re-postgres-image .\web\database
docker volume create PropertySmartDBVol
docker run --name PropertySmartDB -e POSTGRES_PASSWORD=admin -p 5433:5432 -v PropertySmartDBVol:/var/lib/postgresql/data -d re-postgres-image

docker stop PropertySmartDB
docker start PropertySmartDB


docker rm -v PropertySmartDB
docker exec -it PropertySmartDB psql -U admin realestateDB

