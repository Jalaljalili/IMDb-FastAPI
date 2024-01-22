import pandas as pd
from sqlalchemy import create_engine

# Set your PostgreSQL database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'mysecretpassword'
}

def import_data(file_path, table_name, schema, columns, chunk_size=10000):
    # Create a PostgreSQL engine using SQLAlchemy
    engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')

    # Read the TSV file in chunks and append to the PostgreSQL table
    for chunk in pd.read_csv(file_path, delimiter='\t', names=columns, na_values='\\N', chunksize=chunk_size, iterator=True):
        chunk.to_sql(table_name, con=engine, schema=schema, if_exists='append', index=False)

    # Close the database connection
    engine.dispose()

    print(f'Data imported into PostgreSQL table {schema}.{table_name}')

def main():
    # Define column names based on the dataset description
    name_basics_columns = ['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
    title_akas_columns = ['titleId', 'ordering', 'title', 'region', 'language', 'types', 'attributes', 'isOriginalTitle']
    title_basics_columns = ['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes',  'genres']
    title_crew_columns = ['tconst', 'directors', 'writers']
    title_episode_columns = ['tconst', 'parentTconst', 'seasonNumber', 'episodeNumber']
    title_principals_columns = ['tconst', 'ordering', 'nconst', 'category', 'job', 'characters']
    title_ratings_columns = ['tconst', 'averageRating', 'numVotes']
    
    
    # Call the import_data function for each dataset
    import_data('data/name.basics.tsv', 'name_basics', 'public', name_basics_columns)
    import_data('data/title.akas.tsv', 'title_akas', 'public', title_akas_columns)
    import_data('data/title.basics.tsv', 'title_basics', 'public', title_basics_columns)
    import_data('data/title.crew.tsv', 'title_crew', 'public', title_crew_columns)
    import_data('data/title.episode.tsv', 'title_episode', 'public', title_episode_columns)
    import_data('data/title.principals.tsv', 'title_principals', 'public', title_principals_columns)
    import_data('data/title.ratings.tsv', 'title_ratings', 'public', title_ratings_columns)    


if __name__ == '__main__':
    main()
