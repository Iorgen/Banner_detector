# Banner detector App: 

# Development

### 
check before commit 
```
flake8 --ignore=E501,F401,F403,F405 .
```
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

``` Running this command Celery works perfect 
$ celery -A banner_app worker --loglevel=debug -P solo --without-gossip --without-mingle --without-heartbeat
```
 
 
1) install docker docker-compose 
2) clone project 
3) copy models folder to server in banner_app/ folder with all including stuff 
3.1) copy default.jpg to server and then copyy docker cp to container:/media
4) copy output.csv for initial bus loading 
5) docker-compose -f docker-compose.prod.yml up -d --build
6) docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
7) docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic --no-input --clear
8) docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate --noinput
9) docker-compose -f docker-compose.prod.yml exec web python3 manage.py set_groups
10) docker-compose -f docker-compose.prod.yml exec web python3 manage.py bus_parsing


