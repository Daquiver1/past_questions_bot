# Define the application build stage
FROM python:3.11.8-slim-bookworm as app-build

# Set work directory and environment variables
WORKDIR /past_questions_bot
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONBUFFERED=1

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat-openbsd gcc \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY requirements.txt requirements-dev.txt /past_questions_bot/
RUN pip install --upgrade -r requirements.txt -r requirements-dev.txt

# Copy project
COPY . /past_questions_bot

# Use the custom entrypoint script
CMD ["./run_dev.sh"]
