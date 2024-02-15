# Live Site
Check out the live site [here](https://calm-stone-0fb97a700.4.azurestaticapps.net/){:target="_blank"}.

# How to run in local machine
1. Start a new virtual environments and run
```cmd
pip install -r requirements.txt
```


2. Start backend and database docker container
```
docker-compose up
```


3. Crawl data and import it to database
- navigate to adhoc-scripts folder
- update data_folder variable in constants.py and run the following command:
For Windows:
```cmd 
python data_prep.py
```
For Linux:
```bash
python3 data_prep.py
```


4. Start frontend
- navigate to adhoc-scripts folder. Run the following command.
```
npm start
```
