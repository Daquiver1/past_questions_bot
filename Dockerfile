# Define the base image for the build stage
FROM debian:buster-slim as litestream-build

# Download and install Litestream
ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

# Define the application build stage
FROM python:3.11-slim-buster as app-build

# Set work directory and environment variables
WORKDIR /past_questions_bot
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONBUFFERED=1

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY requirements.txt /past_questions_bot/
RUN pip install --upgrade -r requirements.txt

# Copy the Litestream binary from the build stage
COPY --from=litestream-build /usr/local/bin/litestream /usr/local/bin/litestream

# Copy project
COPY . /past_questions_bot

# Use the custom entrypoint script
CMD ["./run_dev.sh"]
