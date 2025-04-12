
import json

class DatabaseConfig:
    host = None
    port = None
    user = None
    password = None
    database = None

class HttpConfig:
    port = 8080
    host = "0.0.0.0"

class LLMConfig:
    address = None
    token = None

class Config:
    # Database configuration
    database: DatabaseConfig = None

    def __init__(self):
        self.database = None

    def load(self, config_file):
        # Load the configuration from the file
        with open(config_file, 'r') as file:
            config = json.load(file)

            self.database = DatabaseConfig()
            self.database.host = config['database']['host']
            self.database.port = config['database']['port']
            self.database.user = config['database']['user']
            self.database.password = config['database']['password']
            self.database.database = config['database']['database']

            self.http = HttpConfig()
            self.http.port = config['http']['port']
            self.http.host = config['http']['host']

            self.llm = LLMConfig()
            self.llm.address = config['llm']['address']
            self.llm.token = config['llm']['token']



            

