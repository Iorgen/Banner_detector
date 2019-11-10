# pull official base image
FROM python:3.6

# set work directory
WORKDIR /usr/src/banner_app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install psycopg2 dependencies
#RUN apt update \
#    && apt add postgresql-dev gcc python3-dev musl-dev

RUN apt-get update && apt-get install -y netcat

# Update pip and from requirements.txt install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/banner_app/requirements.txt
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/banner_app/entrypoint.sh

# copy project
COPY . /usr/src/banner_app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/banner_app/entrypoint.sh"]
CMD ["run"]