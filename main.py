from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, Boolean, Numeric
from sqlalchemy.orm import declarative_base
import pandas as pd
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
import concurrent.futures

# Set your Postgres database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'mysecretpassword'
}

# Define table structures with SQLAlchemy ORM
Base = declarative_base()
# PostgreSQL connection URI
connection_uri = f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}'
# Create a PostgreSQL engine using SQLAlchemy to the default 'postgres' DB
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/postgres')

# Connect to PostgreSQL server
with engine.connect() as conn:
    # Start a transaction
    conn.execute(text('COMMIT'))
    try:
        # Try creating the IMDB database
        conn.execute(text('CREATE DATABASE IMDB'))
        print('Database "IMDB" created successfully.')
    except OperationalError as e:
        print(f"An error occurred: {e.diag.message_primary}")
        
engine.dispose()  # Dispose the connection to the default 'postgres' DB


class NameBasics(Base):
    __tablename__ = 'name_basics'
    nconst = Column(String, primary_key=True)
    primaryName = Column(String)
    birthYear = Column(Integer)
    deathYear = Column(Integer)
    primaryProfession = Column(ARRAY(String))
    knownForTitles = Column(ARRAY(String))

class TitleAkas(Base):
    __tablename__ = 'title_akas'
    titleId = Column(String, primary_key=True)
    ordering = Column(Integer, primary_key=True)
    title = Column(String)
    region = Column(String)
    language = Column(String)
    types = Column(ARRAY(String))
    attributes = Column(ARRAY(String))
    isOriginalTitle = Column(Boolean)
    
class TitleBasics(Base):
    __tablename__ = 'title_basics'
    tconst = Column(String, primary_key=True)
    titleType = Column(String)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    isAdult = Column(Integer)
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(String)
    genres = Column(ARRAY(String))

class TitleCrew(Base):
    __tablename__ = 'title_crew'
    tconst = Column(String, ForeignKey('title_basics.tconst'), primary_key=True)
    directors = Column(String)
    writers = Column(String)

class TitleEpisode(Base):
    __tablename__ = 'title_episode'
    tconst = Column(String, ForeignKey('title_basics.tconst'), primary_key=True)
    parentTconst = Column(String, ForeignKey('title_basics.tconst'))
    seasonNumber = Column(Integer)
    episodeNumber = Column(Integer)

class TitlePrincipals(Base):
    __tablename__ = 'title_principals'
    tconst = Column(String, primary_key=True)
    ordering = Column(Integer, primary_key=True)
    nconst = Column(String)
    category = Column(String)
    job = Column(String)
    characters = Column(String)

class TitleRatings(Base):
    __tablename__ = 'title_ratings'
    tconst = Column(String, ForeignKey('title_basics.tconst'), primary_key=True)
    averageRating = Column(Numeric)
    numVotes = Column(Integer)


# Function to create tables with defined foreign keys and relationships
def create_tables(engine):
    Base.metadata.create_all(engine)

def preprocess_array_values(column_values):
    return column_values.apply(lambda x: None if pd.isnull(x) else '{' + ','.join(str(val) for val in x.split(',')) + '}')

def preprocess_boolean_values(column_values):
    return column_values.apply(lambda x: True if x == '1' else False if x == '0' else None)

def preprocess_year_values(column_values):
    return pd.to_numeric(column_values, errors='coerce')

def import_data(file_path, table_name, schema, columns, chunk_size, preprocessors=None):
    engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/imdb')
    first_chunk = True
    for chunk in pd.read_csv(file_path, delimiter='\t', names=columns, na_values='\\N', chunksize=chunk_size, iterator=True, skiprows=1 if first_chunk else None):
        if preprocessors:
            for column, preprocessor in preprocessors.items():
                chunk[column] = preprocessor(chunk[column])

        try:
            chunk.to_sql(table_name, con=engine, schema=schema, if_exists='append', index=False, method='multi')
        except Exception as e:  # Broad exception to catch all errors
            # It is useful to log the offending data and the error message.
            with open(f'{table_name}_import_errors.log', 'a') as f:
                f.write(f'Error importing data: {e}\n')
               # f.write(chunk.to_csv(index=False))
            print(f"An error occurred during data import for table {table_name}: {e}")
            continue
    print(f'Data imported into PostgreSQL table {schema}.{table_name}')
    engine.dispose()


def main():
    
    engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/imdb')
    create_tables(engine)
    
    name_basics_columns = ['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
    title_akas_columns = ['titleId', 'ordering', 'title', 'region', 'language', 'types', 'attributes', 'isOriginalTitle']
    title_basics_columns = ['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres']
    title_crew_columns = ['tconst', 'directors', 'writers']
    title_episode_columns = ['tconst', 'parentTconst', 'seasonNumber', 'episodeNumber']
    title_principals_columns = ['tconst', 'ordering', 'nconst', 'category', 'job', 'characters']
    title_ratings_columns = ['tconst', 'averageRating', 'numVotes']

    import_data('data/name.basics.tsv', 'name_basics', 'public', name_basics_columns, 10000, preprocessors={
        'primaryProfession': preprocess_array_values,
        'knownForTitles': preprocess_array_values,
        'birthYear': preprocess_year_values,
        'deathYear': preprocess_year_values
    })
    
    import_data('data/title.basics.tsv', 'title_basics', 'public', title_basics_columns, 10000, preprocessors={
    'genres': preprocess_array_values,
    'startYear': preprocess_year_values,
    'endYear': preprocess_year_values
    })
    
    import_data('data/title.akas.tsv', 'title_akas', 'public', title_akas_columns, 10000, preprocessors={
        'types': preprocess_array_values,
        'attributes': preprocess_array_values,
        'isOriginalTitle': preprocess_boolean_values
    })

    import_data('data/title.crew.tsv', 'title_crew', 'public', title_crew_columns, 10000, preprocessors={
    'directors': preprocess_array_values,
    'writers': preprocess_array_values
    })
    
    import_data('data/title.episode.tsv', 'title_episode', 'public', title_episode_columns, 10000, preprocessors={
    'seasonNumber': preprocess_year_values,
    'episodeNumber': preprocess_year_values
    })

    import_data('data/title.principals.tsv', 'title_principals', 'public', title_principals_columns, 10000, preprocessors={
    'characters': preprocess_array_values
    })

    import_data('data/title.ratings.tsv', 'title_ratings', 'public', title_ratings_columns, 10000)


    engine.dispose()

if __name__ == '__main__':
    main()