# Readme

Hey there! Welcome to our ETL project, where we use Docker to create event-driven architectures for ETL processes in Python, using MongoDB and MySQL with RabbitMQ queues.

Our main goal is to connect to MongoDB, transform the data, and load it into a MySQL-based business intelligence system, with the added bonus of handling events through RabbitMQ queues, making our project efficient and reliable.

Here are the steps to deploy and test your worker in both development and production environments:

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
    
We hope you enjoy working with our project and find it helpful. If you have any questions or concerns, please feel free to reach out to us. Happy coding!
