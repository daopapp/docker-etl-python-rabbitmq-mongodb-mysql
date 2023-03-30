FROM python:3.7

# Install Supervisor
RUN apt-get update && \
    apt-get install -y supervisor

# Copy application files
COPY requirements.txt /app/
COPY .env /app/
COPY . /app/

# Install application dependencies
WORKDIR /app
RUN pip install -r requirements.txt

# Start Supervisor when the container starts
CMD service supervisor start; /bin/bash
