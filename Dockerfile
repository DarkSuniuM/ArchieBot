FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev cron

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

# Set crontab
RUN echo '*/30 * * * * cd /app && python3 automated.py' >> temp_cron

RUN crontab temp_cron

RUN rm temp_cron
# Set crontab

ENTRYPOINT [ "python3" ]

# Do the database upgrades
RUN alembic upgrade head

CMD [ "app.py" ]
