# Banner detector App: 

# Development
### Delete all unused dockers 
```
docker rmi $(docker images -q -f "dangling=true")
```
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
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py set_groups --no  -input --clear
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
```

- how to kill postgresql database 
``
$ docker-compose down --remove-orphans --volumes
``
# Deploy Rebuild django server: 

```
$ docker-compose -f docker-compose.prod.yml up -d --no-deps --build web 
# If needed to set migrate 
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic --no-input --clear
```

# Command for looking at full logs and errors 
```
$ docker logs --tail 50 --follow --timestamps celery_worker
```
 