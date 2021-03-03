
# Backend API  
API for vMeeting project  
# Config  
- Set environment variable for Database URI  
	> Example:    
	 {database_uri} for Postgres:  postgres+psycopg2://username:password@localhost/host  
  
	```  
	$ export DATABASE_URI='{database_uri}'  
	```  
	  
- Set environment variable for secret key  
	```  
	$ export SECRET='{secret_key}'  
	```  
- Set environment variable for Google credentials  
	> Example:    
	> {redirect_uri}: http://localhost:1234    
	> {client_id}: 687171305927-i344oubmrt0g58ouebtpr7056ae2XXXX.apps.googleusercontent.com    
	> {client_secret}: v9fWTXvV8ja57q1A_w6XXXX  
	```  
	$ export REDIRECT_URI='{redirect_uri}'  
	$ export CLIENT_ID='{client_id}'  
	$ export CLIENT_SECRET='{client_secret}'  
	```  
- Set up time config.    
	> Default:    
	> {time_difference}:  Default is 7 hours 
	> {time_delay}: Default is 600 seconds
	```  
	$ export TIME_DIFFERENCE='{time_difference}'  
	$ export CALENDAR_UPDATE_DELAY='{time_delay}'
	```  
  
- Set up Celery config  
    > Example:    
    > {broker_url}: redis://localhost:6379/0    
    > {result_backend}: redis://localhost:6379/0    
    > {result_backend}: json  
	 ```  
	 $ export CELERY_BROKER_URL='{broker_url}'  
	 $ export CELERY_RESULT_BACKEND='{result_backend}' 
	 $ export CELERY_TASK_SERIALIZER='{result_backend}'
	 ```  
- Set up SMTP
    ```  
	 $ export EMAIL_ACCOUNT='{email_account}'  
	 $ export SMTP_USERNAME='{smtp_username}' 
	 $ export SMTP_PASSWORD='{smtp_password}'
	 $ export SMTP='{smtp}'
	 $ export SMTP_PORT='{smtp_port}'
	 ```  
  
# Setup  
  
Install pepenv and load the dependencies  
```  
$ pip install pipenv  
$ pipenv install  
$ pipenv shell  
```  
  
# Database initialization  
  
Create the database  
```  
$ alembic upgrade head  
```  
  
Initialize database  
```  
$ ipython  
In [1]: from seed import Seeder  
In [2]: from src.database import PostgresConnector  
In [3]: import os  
In [4]: os.environ["DATABASE_URI"] = '{database_uri}'  
In [5]: db = PostgresConnector(os.getenv('DATABASE_URI'))  
In [6]: seeder = Seeder(db)  
In [7]: seeder.init_db()  
```  
Or   
```  
$ ipython  
In [1]: from seed import init_db  
```  
  
  
Create location  
```  
$ ipython  
In [7]: seeder.create_location()  
```  
  
  
# Requirements  
Pipfile  
  
# Run  
Web api  
```sh  
$ uwsgi --protocol=http --http-socket=127.0.0.1:5000 --callable=app --wsgi-file=web_api.py --lazy-apps --processes=5  
```  
  
  
# Run Celery   
```
celery -A  web_api.celery worker  
```