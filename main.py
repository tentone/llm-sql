import pypyodbc 
import pandas as pd

cnxn = pypyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"\
                        "Server=localhost;"\
                        "Database=database;"\
                        "uid=user;"\
                        "pwd=password")


df = pd.read_sql_query('select * from table', cnxn)