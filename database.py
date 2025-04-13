import re
import pypyodbc
import config

class Database:
    cfg: config.Config

    conn: pypyodbc.Connection

    def __init__(self, cfg: config.Config):
        self.cfg = cfg
        self.conn = None

    def connect(self)-> None:
        # Database connection configuration
        driver = "ODBC Driver 18 for SQL Server"
        connection = f"DRIVER={driver};SERVER={self.cfg.database.host},{self.cfg.database.port};DATABASE={self.cfg.database.database};UID={self.cfg.database.user};PWD={self.cfg.database.password}"

        print(f"Connecting to database {connection}")

        # Connect to the database using the configuration
        self.conn = pypyodbc.connect(connection)
        

    def close(self)-> None:
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def query(self, sql)-> list[any]:
        if not self.conn:
            raise Exception("Database connection is not established.")
        
        cursor = self.conn.cursor()
        cursor['execute'](sql)
        result = cursor['fetchall']()
        cursor['close']()
        return result

    def database_structure(self)-> None:
        """
        Get the structure of the database in a readable format to  be teached to the LLM
        """
        if not self.conn:
            raise Exception("Database connection is not established.")
    
        query = """SELECT 
            t.name AS table_name,
            c.name AS column_name,
            ty.name AS data_type,
            i.name AS index_name,
            i.type_desc AS index_type,
            fk.name AS fk_name,
            rt.name AS fk_table,
            rc.name AS fk_column
        FROM sys.tables t
        JOIN sys.columns c ON t.object_id = c.object_id
        JOIN sys.types ty ON c.user_type_id = ty.user_type_id
        LEFT JOIN sys.index_columns ic ON ic.object_id = t.object_id AND ic.column_id = c.column_id
        LEFT JOIN sys.indexes i ON i.object_id = t.object_id AND i.index_id = ic.index_id
        LEFT JOIN sys.foreign_key_columns fkc  ON fkc.parent_object_id = t.object_id AND fkc.parent_column_id = c.column_id
        LEFT JOIN sys.foreign_keys fk ON fk.object_id = fkc.constraint_object_id
        LEFT JOIN sys.tables rt ON rt.object_id = fkc.referenced_object_id
        LEFT JOIN sys.columns rc  ON rc.object_id = fkc.referenced_object_id AND rc.column_id = fkc.referenced_column_id
        ORDER BY t.name, c.column_id;"""

        # Execute the query to get the database structure
        cursor = self.conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        
        # List to store the table names and their columns
        tables: map[any] = {}

        # Iterate through the records and build the table structure
        for r in records:
            # Check if table is included in the include list
            if len(self.cfg.database.include) == 0 or not any(re.match(pattern, r['table_name']) for pattern in self.cfg.database.include):
                continue

            # Check if the table name matches any of the exclusion patterns
            if any(re.match(pattern, r['table_name']) for pattern in self.cfg.database.exclude):
                continue

            if r['table_name'] not in tables:
                tables[r['table_name']] = []

            # Check if column already exists in the table
            column_exists = any(col['column'] == r['column_name'] for col in tables[r['table_name']])

            # Edit the column if it exists
            if column_exists:
                # Check if the column already exists in the table, pk and fk will be duplicated in the list
                for col in tables[r['table_name']]:
                    if col['column'] == r['column_name']:
                        if not col['pk']:
                            col['pk'] = False if r['index_name'] is None else True if "pk" in r['index_name'] else False
                        if not col['fk']:
                            col['fk'] = False if r['fk_name'] is None else True
                            col['fk_table'] = r['fk_table'] if r['fk_table'] is not None else None
                            col['fk_column'] = r['fk_column'] if r['fk_column'] is not None else None
            else:
                tables[r['table_name']].append({
                    "column": r['column_name'],
                    "type": r['data_type'],
                    "pk": False if r['index_name'] is None else True if "pk" in r['index_name'] else False,
                    "fk": False if r['fk_name'] is None else True,
                    "fk_table": r['fk_table'] if r['fk_table'] is not None else None,
                    "fk_column": r['fk_column'] if r['fk_column'] is not None else None,
                })
    
        # Prepare the prompt for the LLM
        prompt = "The database has the following tables and columns:\n\n"
        for table, columns in tables.items():
            prompt += f"{table}:\n"
            for column in columns:
                prompt += f"\t- {column['column']} ({column['type']})"
                if column['pk']:
                    prompt += f" - pk"
                if column['fk']:
                    prompt += f" - fk"
                    if column['fk_table']:
                        prompt += f" - {column['fk_table']}({column['fk_column']})"
                prompt += "\n"
            prompt += "\n"

        return prompt
