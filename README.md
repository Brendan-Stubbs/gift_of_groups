# gift_of_groups
A web application to manage group birthday gifts

### Set up virtual environment
Make sure you have Python 3 installed

Install the virtual environment library
```
pip3 install virtualenv
```
Set up a file to contain your virtual environments
```
cd ~
mkdir Venvs
```

Install your virtual environment
```
cd Venvs
python3 -m virtualenv gift-of-groups
```

Activate your virtual environment and install dependencies on Mac / Linux
```
source ~/Venvs/gift-of-groups/bin/activate
pip install -r requirements.txt
```

Activate your virtual enviornment on Windoes
```
~/Venvs/gift-of-groups/Scripts/activate.bat
```

### Set up local_settings.py in the same directory as settings.py
```
DEBUG = True
ENVIRONMENT = "local"
SECRET_KEY = <See below>
```
Set the value of secret key as the result of
```
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

**If you would like to use psql. Else you can ignore and it will default to sqlite**
Install Postgres SQL and create a database
```
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```

~~~
sudo -u postgres psql
~~~

~~~
CREATE USER gift_user with PASSWORD 'iamthetestdb';
CREATE DATABASE gift_db;
GRANT ALL PRIVILEGES ON DATABASE gift_db to gift_user;
~~~

Add the following to your local_settings.py file
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "gift_db",
        "USER": "gift_user",
        "PASSWORD": "iamthetestdb",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```
**end psql section**


Run the existing migrations
```
python manage.py migrate
```

Run local server
```
python mange.py runserver
```

**Running with Docker**  
```bash
  docker-compose up --build
```