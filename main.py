import pypyodbc 
import pandas as pd

cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"
                        "Database=database;"
                        "uid=user;pwd=password")


df = pd.read_sql_query('select * from table', cnxn)