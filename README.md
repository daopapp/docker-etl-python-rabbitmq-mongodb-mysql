# Readme

## Description
    This project is a Docker-based solution for creating ETL processes in Python, using MongoDB and MySQL, with RabbitMQ queues. 
    The main goal of the project is to connect to a MongoDB database, transform the data, and load it into a MySQL-based business intelligence system. 
    The project is designed to handle event-driven architectures, with data processing taking place through a RabbitMQ queue rather than as a massive, full-database consumption.

## Deployment instructions

### Requirements
    1. Docker

### Instructions 
    1. Setup your environment variables in `.env` file (see `.env.example`)
    1. Build docker `docker-compose up -d`
    2. Run docker `docker-compose exec app python <your_file>`

### Run Dev
    1. The big difference between dev and prod is that dev doesn't start the supervisor automatically
    2. So, to test your worker, you need to run inside your docker the python file that you want to test

### Run Prod
    1. The big difference between dev and prod is that prod starts the supervisor automatically
    2. So, to test your worker, you need to run inside your docker the python file that you want to test

### Makefile
    1. You can use the Makefile to run the commands above
    2. `make build` to build the docker
    4. `make dev` to run the docker in dev mode
    5. `make start` to run the docker in prod mode

### Supervisor
    1. The supervisor is a process manager that will run your workers
    2. For each worker you need to create a file in `supervisor/conf.d/` folder
    3. The file name must be `<your_worker_name>.conf`

### Test your worker
    1. To test your worker, you need to create a python file inside `test` folder
    2. The file must be the rabbitmq connection and the worker that you want to test