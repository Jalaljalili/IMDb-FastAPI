import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Set your PostgreSQL database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'mysecretpassword'
}

# Set the path to your IMDb dataset TSV file
file_path = 'data/name.basics.tsv'

# Define the PostgreSQL table schema and name
table_name = 'name_basics'
schema = 'public'  # You can change this to your desired schema

# Define column names based on the dataset description
columns = ['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']

# Define chunk size (adjust as needed)
chunk_size = 10000

# Create a PostgreSQL engine using SQLAlchemy
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')

# Read the TSV file in chunks and append to the PostgreSQL table

for chunk in pd.read_csv(file_path, delimiter='\t', names=columns, na_values='\\N', chunksize=chunk_size, iterator=True):
    chunk.to_sql(table_name, con=engine, schema=schema, if_exists='append', index=False)

# Optional: Commit changes if needed
# engine.connect().execute('COMMIT')

# Close the database connection
engine.dispose()

print(f'Data imported into PostgreSQL table {schema}.{table_name}')
