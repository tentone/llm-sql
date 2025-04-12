import pypyodbc 
import pandas as pd
import config

cfg = config.Config()
cfg.load('config.json')

db = pypyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"\
                        "Server=localhost;"\
                        "Database=database;"\
                        "uid=user;"\
                        "pwd=password")


df = pd.read_sql_query('select * from table', db)