# Giftly Groups
A web application to manage group birthday gifts



### Set up local_settings.py in the same directory as settings.py
```
DEBUG = True
ENVIRONMENT = "local"
SECRET_KEY = 'somesecret'
PATREON_SECRET = "somesecret"
BUY_ME_A_COFFEE_SECRET = "somesecret"
DOMAIN_NAME = "https://www.giftlygroups.com/"
EMAIL_HOST_PASSWORD = "somepassword"
EMAIL_HOST_USER = "giftlygroups@gmail.com"
ACTIVATE_EMAIL_ON_ENVIRONMENT = False
```


**Running with the app**  
Ensure you have [docker](https://www.docker.com/products/docker-desktop/) installed
```bash
  docker-compose up --build
```
Access the app on http://localhost:8090

**Installing new packages**
```bash
# -u 0 to run as root user
docker exec -u 0 -it gift_of_groups_giftly_groups_1 pip install <package>

# Update requirements.txt
docker exec -u 0 -it gift_of_groups_giftly_groups_1 pip freeze > requirements.txt
```

**Making and applying migrations**
```bash
# Make the migrations
docker exec -it gift_of_groups_giftly_groups_1 python manage.py makemigrations

# Apply the migrations
docker exec -it gift_of_groups_giftly_groups_1 python manage.py migrate
```
