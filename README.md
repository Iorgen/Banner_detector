# Banner detector App: 
run docker-compose up -d 

# postqres + django + nginx: 
https://www.howtoforge.com/tutorial/how-to-install-django-with-postgresql-and-nginx-on-ubuntu-16-04/

# Текущие конечные задачи: 
# FrontEnd Tasks: 
1) Billboard page 
1.1) Image Editor for billboards.
2) Мобильная версия (есть необходимы минимальные изменения).
3) AJAX list banner types 

# BackEnd tasks: 
6) date time format for xml export

### cleaner code tasks: 
2) Logging 
3) Exceptions Handling 

### Pre Deploy tasks: 
0) change all passwords to not my 
1) Deploy - docker configuration 
2) Check all User permissions 
3) Estimate ML accuracy. 


## Workers start :
## redis :
 + docker run -p 6379:6379 -d redis:2.8    
## Celery workers :
 + celery -A banner_app worker -l info

### Tutorials : 
https://medium.com/@bencleary/django-scheduled-tasks-queues-part-2-fc1fb810b81d 
https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
https://www.techiediaries.com/python-django-ajax/
https://realpython.com/django-and-ajax-form-submissions/
https://code.djangoproject.com/wiki/AJAX

### Crontab celery configurations tutorial 
https://www.codingforentrepreneurs.com/blog/celery-redis-django

http://fabricjs.com/
# Algorithm 
create superuser
create then user with admin privilegies 
create groups worker and manager

# При запуске модели собирать датасет 
собирать датасет 
Заняться разметкой (возможно отдать это на сторону)
съёмка с камеры 

# postgres setting up 
sudo su - postgres
psql
CREATE USER with encodnidg and privileges;
CREATE TABLE table_name OWNER user;

# Fonts library 
https://useiconic.com/open/

# Deploy instructions 
- Setting up development server 
```
$ docker-compose build
$ docker-compose up -d
# Updare permissions 
$ chmod +x app/entrypoint.sh
```

- Setting up production server 
```
clone from repo from https://github.com/Iorgen/Banner_detector.git + 
scp all banner_app/models to banner_app/models + 
scp all static from detector_app/static to detector_app/static/ + 
Copy files default.jpg from media to image(web) media  
set server_name inside nginx.conf 
```
- Run following commands for starting server 
```
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate --noinput 
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic --no-input --clear
$ docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
```
#### how to kill postgresql data 
docker-compose down --remove-orphans --volumes