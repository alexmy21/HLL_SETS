import os
import yaml
import pandas as pd
import pyarrow as pa
from pykwalify.core import Core

import duckdb

class HsetCore: 
    # def __init__(self, source_file=None, source_data=None, schema_files=None, schema_data=None, extensions=None, c=None, schema=None, source=None):
    #     self.source_file = source_file
    #     self.source_data = source_data
    #     self.schema_files = schema_files
    #     self.schema_data = schema_data
    #     self.extensions = extensions
    #     self.c = c
    #     self.schema = schema
    #     self.source = source   

    #===========================================================================
    # YAML
    #===========================================================================
    def yaml(self, yaml_file):
        with open(yaml_file, 'r') as f:
            return yaml.safe_load(f)
    
    def yaml_to_string(self, data):
        return yaml.dump(data)
    
    def yaml_file_to_string(self, yaml_file):
        with open(yaml_file, 'r') as f:
            return yaml.dump(f)
        
    def yaml_string_to_file(self, yaml_string, yaml_file):
        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_string, f)

    def yaml_to_pd_df(self, yaml_file):
        # Load YAML data into a Python data structure
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        # Convert the Python data structure into a pandas DataFrame
        return pd.DataFrame(data)
    
    def yaml_file_to_arrow(self, yaml_file):
        # Load YAML data into a Python data structure
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        # Convert the Python data structure into a pandas DataFrame
        df = pd.DataFrame(data)
        # Convert the pandas DataFrame into an Arrow table
        return pa.Table.from_pandas(df)

    def yaml_string_to_arrow(self, yaml_string):
        # Load YAML string into a Python data structure
        data = yaml.safe_load(yaml_string)
        # Convert the Python data structure into a pandas DataFrame
        df = pd.DataFrame(data)
        # Convert the pandas DataFrame into an Arrow table
        return pa.Table.from_pandas(df)

    def validate_yaml_file(self, yaml_file, schema_file):
        c = Core(source_file=yaml_file, schema_files=[schema_file])
        return c.validate()

    def validate_yaml(self, yaml_string, schema_file):
        c = Core(source_data=yaml_string, schema_files=[schema_file])
        return c.validate()
    
#===============================================================================
# DuckDB (ddb)
#===============================================================================
    def create_ddb_table_df(self, table_name, data, conn):
        # Convert the pandas DataFrame into an Arrow table
        table = pa.Table.from_pandas(data)
        # Write the Arrow table to the Arrow file
        pa.write_table(table, 'data.arrow')
        # Create a DuckDB table from the Arrow file
        conn.execute(f'CREATE TABLE {table_name} AS (SELECT * FROM read_arrow_auto(\'data.arrow\'))')
        # Remove the Arrow file
        os.remove('data.arrow')

    def create_ddb_table_yaml(self, table_name, yaml_file, conn):
        # Load YAML data into a Python data structure
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        # Convert the Python data structure into a pandas DataFrame
        df = pd.DataFrame(data)
        # Convert the pandas DataFrame into an Arrow table
        table = pa.Table.from_pandas(df)
        # Write the Arrow table to the Arrow file
        pa.write_table(table, 'data.arrow')
        # Create a DuckDB table from the Arrow file
        conn.execute(f'CREATE TABLE {table_name} AS (SELECT * FROM read_arrow_auto(\'data.arrow\'))')
        # Remove the Arrow file
        os.remove('data.arrow')

    def append_yaml_to_ddb_table(self, table_name, yaml_file, conn):
        # Load YAML data into a Python data structure
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        # Convert the Python data structure into a pandas DataFrame
        df = pd.DataFrame(data)
        # Convert the pandas DataFrame into an Arrow table
        table = pa.Table.from_pandas(df)
        # Write the Arrow table to the Arrow file
        pa.write_table(table, 'data.arrow')
        # Append the data from the Arrow file to the existing DuckDB table
        conn.execute(f'INSERT INTO {table_name} SELECT * FROM read_arrow_auto(\'data.arrow\')')
        # Remove the Arrow file
        os.remove('data.arrow')

    def append_df_to_ddb_table(self, table_name, data, conn):
        # Convert the pandas DataFrame into an Arrow table
        table = pa.Table.from_pandas(data)
        # Write the Arrow table to the Arrow file
        pa.write_table(table, 'data.arrow')
        # Append the data from the Arrow file to the existing DuckDB table
        conn.execute(f'INSERT INTO {table_name} SELECT * FROM read_arrow_auto(\'data.arrow\')')
        # Remove the Arrow file
        os.remove('data.arrow')

    def persist_ddb_table(conn, disk_db_path, table_name):
        # Connect to the disk-based DuckDB
        disk_conn = duckdb.connect(disk_db_path)
        # Check if the table exists in the disk-based DuckDB
        result = disk_conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if result.fetchone() is None:
            # If the table doesn't exist, create it by copying the structure of the in-memory table
            disk_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name} WHERE 0", con=conn)
        # Append the data from the in-memory table to the disk-based table
        disk_conn.execute(f"INSERT INTO {table_name} SELECT * FROM {table_name}", con=conn)
        # close the disk-based DuckDB connection
        disk_conn.close()

    def restore_ddb_table(conn, disk_db_path, table_name):
        # Connect to the disk-based DuckDB
        disk_conn = duckdb.connect(disk_db_path)
        # Check if the table exists in the disk-based DuckDB
        result = disk_conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if result.fetchone() is None:
            # If the table doesn't exist, create it by copying the structure of the in-memory table
            disk_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name} WHERE 0", con=conn)
        # Append the data from the in-memory table to the disk-based table
        disk_conn.execute(f"INSERT INTO {table_name} SELECT * FROM {table_name}", con=conn)
        # close the disk-based DuckDB connection
        disk_conn.close()


# Validate your YAML file
print(HsetCore().validate_yaml_file('data/test.yaml', 'data/schema.yaml'))
