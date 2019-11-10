# Banner detector App: 

# Development

### async recognition tasks
```
# start redis 
$ docker run -p 6379:6379 -d redis:2.8    
# start worker
$ celery -A banner_app worker -l info
```
 
# Algorithm 
create superuser
create groups worker and manager

# postgres setting up 
```
sudo su - postgres
psql
CREATE USER with encodnidg and privileges;
CREATE TABLE table_name OWNER user;
```

- Setting up development docker-compose
```
$ docker-compose build
$ docker-compose up -d
# Updare permissions 
$ chmod +x app/entrypoint.sh
```

# Deploy: 

- Setting up production server 
```
clone from repo from https://github.com/Iorgen/Banner_detector.git + 
scp all banner_app/models to banner_app/models + 
scp all static from detector_app/static to detector_app/static/ + 
Copy files default.jpg from media to image(web) media  
# Example 
docker cp ../default.jpg bdfa613b4293:/home/banner_app/web/media
set server_name inside nginx.conf 
```
- Run following commands for starting server 
```
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate --noinput 
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic --no-input --clear
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
```
- how to kill postgresql database 
``
$ docker-compose down --remove-orphans --volumes
``


# Additional info 

### The best django + docekr + nginx deploy tutorial  
 - https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

### celery + redis  : 
 - https://medium.com/@bencleary/django-scheduled-tasks-queues-part-2-fc1fb810b81d 
 - https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
 - https://www.codingforentrepreneurs.com/blog/celery-redis-django

### Canvas library 
 - http://fabricjs.com/

### Fonts library 
 - https://useiconic.com/open/