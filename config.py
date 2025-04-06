
import json

class DatabaseConfig:
    # Database configuration
    host = None
    port = None
    user = None
    password = None
    database = None


class Config:
    # Database configuration
    database: DatabaseConfig = None

    def __init__(self):
        self.database = None

    def load(self, config_file):
        # Load the configuration from the file
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.database = config.get('database', None)