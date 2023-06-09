import sshtunnel
import pymysql.cursors
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv
import io
import paramiko
import random

load_dotenv()

db_mongo_host = os.getenv("DB_MONGO_HOST")
db_mongo_port = int(os.getenv("DB_MONGO_PORT"))
db_mysql_port = int(os.getenv("DB_MYSQL_PORT"))
ssh_user = os.getenv("SSH_USER")
db_mysql_host = os.getenv("DB_MYSQL_HOST")
db_mysql_user = os.getenv("DB_MYSQL_USER")
db_mysql_password = os.getenv("DB_MYSQL_PASSWORD")
db_mysql_db = os.getenv("DB_MYSQL_DB")
db_mysql_use_ssh = os.getenv("DB_MYSQL_USE_SSH")
pem_key_str = os.getenv("PEM_KEY")
pem_key_file = io.StringIO(pem_key_str)
pem_key = paramiko.RSAKey.from_private_key(pem_key_file)


class MongoDB:
    _tunnel = None

    def __init__(self, collection_name, db_name, ssh_host=db_mongo_host, ssh_username=ssh_user, ssh_pkey=pem_key):
        self.ssh_host = ssh_host
        self.ssh_username = ssh_username
        self.ssh_pkey = ssh_pkey
        self.db_name = db_name
        self.collection_name = collection_name

        self._create_connection()

    def _create_connection(self):
        if MongoDB._tunnel is None or not MongoDB._tunnel.is_active:
            # Set the range of ports to use
            local_port = range(10000, 20000)

            # Choose a random port from the range
            port = random.choice(local_port)
            MongoDB._tunnel = SSHTunnelForwarder(
                (self.ssh_host, 22),
                ssh_username=self.ssh_username,
                ssh_pkey=self.ssh_pkey,
                remote_bind_address=('127.0.0.1', db_mongo_port),
                local_bind_address=('127.0.0.1', port)
            )
            MongoDB._tunnel.start()
            print('Conexão SSH estabelecida Mongo')

        elif MongoDB._tunnel.is_active:
            print('Reutilizando conexão SSH estabelecida Mongo')

        # Conexão com o MongoDB usando a porta tunelada
        client = MongoClient('localhost', port=MongoDB._tunnel.local_bind_port)
        self.db = client[self.db_name]
        self.collection = self.db[self.collection_name]

    def find_data(self, query=None, limit=False, fields=None):
        projection = fields or {}
        query = query or {}

        if limit:
            return list(self.collection.find(query, projection).limit(limit))

        return list(self.collection.find(query, projection))


    def close_connection(cls):
        if cls._tunnel:
            cls._tunnel.stop()
            print('Conexão SSH encerrada Mongo')


class SSHMySQL:
    def __init__(self, ssh_host=db_mysql_host, ssh_username=ssh_user, ssh_pkey_path=pem_key, mysql_host='127.0.0.1',
                 mysql_user=db_mysql_user, mysql_password=db_mysql_password, mysql_db=db_mysql_db):
        self.ssh_host = ssh_host
        self.ssh_username = ssh_username
        self.ssh_pkey_path = ssh_pkey_path
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.server = None
        self.connection = None

    def start_ssh_tunnel(self):
        # Inicia o túnel SSH se ainda não estiver estabelecido
        if self.server is None and self.server.is_active:
            self.server = sshtunnel.SSHTunnelForwarder(
                ssh_address_or_host=(self.ssh_host, 22),
                ssh_username=self.ssh_username,
                ssh_pkey=self.ssh_pkey_path,
                local_bind_address=('127.0.0.1', db_mysql_port),
                remote_bind_address=(self.mysql_host, db_mysql_port)
            )
            self.server.start()
            print('Conexão SSH estabelecida Mysql')

    def stop_ssh_tunnel(self):
        # Encerra o túnel SSH se estiver aberto
        if self.server is not None and self.server.is_active:
            self.server.stop()

    def open_connection_mysql(self):
        if self.connection is not None and self.connection.open:
            return self.connection
        else:
            # Inicia o túnel SSH se ainda não estiver estabelecido e retorna a conexão com o MySQL
            mhost = db_mysql_host
            mport = db_mysql_port
            if db_mysql_use_ssh == 'true':
                self.start_ssh_tunnel()
                mhost = 'localhost'
                mport = self.server.local_bind_port
            self.connection = pymysql.connect(
                host=mhost,
                user=self.mysql_user,
                password=self.mysql_password,
                database=self.mysql_db,
                port=mport,
                cursorclass=pymysql.cursors.DictCursor,
            )
            print('Conexão Mysql efetuada')
            return self.connection

    def close_connection_mysql(self):
        # Encerra a conexão com o MySQL se estiver aberta e o túnel SSH se estiver aberto
        if self.connection is not None and self.connection.open:
            self.connection.close()
        if db_mysql_use_ssh == 'true':
            self.stop_ssh_tunnel()
