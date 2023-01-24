# gift_of_groups
A web application to manage group birthday gifts



### Set up local_settings.py in the same directory as settings.py
```
DEBUG = True
ENVIRONMENT = "local"
SECRET_KEY = "my_super_secret_key"
```


**Running with the app**  
Ensure you have [docker](https://www.docker.com/products/docker-desktop/) installed
```bash
  docker-compose up --build
```
Access the app on http://localhost:8090
