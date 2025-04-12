import pypyodbc
import pandas as pd
import config

class Database:
    config: config.Config

    connection: pypyodbc.Connection

    def __init__(self, cfg: config.Config):
        self.config = cfg
        self.connection = None

    def connect(self)-> None:
        # Connect to the database using the configuration
        self.connection = pypyodbc.connect(f"Driver={{ODBC Driver 18 for SQL Server}};"
                                           f"Server={self.config.database.host};"
                                           f"Database={self.config.database.database};"
                                           f"uid={self.config.database.user};"
                                           f"pwd={self.config.database.password}")
        
    def close(self)-> None:
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def query(self, sql)-> list[any]:
        if not self.connection:
            raise Exception("Database connection is not established.")
        
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

