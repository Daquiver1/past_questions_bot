FROM python:3.11-slim-buster

# set work directory and environment variables
WORKDIR /past_questions_bot
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

# install & upgrade system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install project dependencies
COPY requirements.txt /past_questions_bot/
RUN pip install --upgrade -r requirements.txt

# copy project
COPY . /past_questions_bot

RUN ["chmod", "+x", "./run_dev.sh"]
CMD ./run_dev.sh