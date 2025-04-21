
import json

class DatabaseConfig:
    host = None
    port = 1433
    user = None
    password = None
    database = None
    include = []
    exclude = []
    sample_data = False

class LLMConfig:
    token = None

class Config:
    # Debug flag
    debug: bool = False

    # Database configuration
    database: DatabaseConfig = None

    # OpenAI config
    llm: LLMConfig = None

    def __init__(self):
        self.database = None

    def load(self, config_file):
        # Load the configuration from the file
        with open(config_file, 'r') as file:
            config = json.load(file)

            self.debug = config['debug']

            self.database = DatabaseConfig()
            self.database.host = config['database']['host']
            self.database.port = config['database']['port']
            self.database.user = config['database']['user']
            self.database.password = config['database']['password']
            self.database.database = config['database']['database']
            self.database.include = config['database']['include']
            self.database.exclude = config['database']['exclude']
            self.database.sample_data = config['database']['sampleData']

            self.llm = LLMConfig()
            self.llm.token = config['openai']['token']



            

