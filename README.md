# How to install

```bash
pip install -r requirements.txt
docker run --rm -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome

```
# How to run

0. Crawl the data
python crawl_realestate.py
python crawl_suburb_profile.py
python crawl_school.py


To start
1. Start the virtual environments
- realestate_env\Scripts\activate

1. Start database on docker
- docker start RePostgresContainer
- Port to access this container on local machine is 5433

2. Run backend
- Navigate to .\web\backend\
- Run the following:
    uvicorn .\web\backend\main:app --reload

3. Start frontend
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

