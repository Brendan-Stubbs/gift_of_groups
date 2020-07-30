# gift_of_groups
A web application to manage group birthday gifts

Set up virtual environment

Make sure you have Python 3 installed

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

Activate your virtual environment and install dependencies
```
source ~/Venvs/gift-of-groups/bin/activate
pip install -r requirements.txt
```

Run the existing migrations
```
python manage.py migrate
```

Run local server
```
python mange.py runserver
```
