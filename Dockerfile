FROM python:3.7
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY .env /app/.env
#RUN pip install --upgrade mysql-connector-python
#COPY . /app
ENTRYPOINT ["python"]

# Install Supervisor
RUN apt-get update && \
    apt-get install -y supervisor && \
    mkdir -p /var/log/supervisor

# Copy all Supervisor configuration files
COPY ./supervisor/*.conf /etc/supervisor/conf.d/

# Start Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
#