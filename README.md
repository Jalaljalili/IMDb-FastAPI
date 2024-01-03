# IMDb-FastAPI
implementation FastAPI for IMDb Non-Commercial Datasets
## IMDb Non-Commercial Datasets Import Script

This Python script is designed to import the IMDb Non-Commercial Datasets into a PostgreSQL database. The datasets are provided in tab-separated-values (TSV) formatted files. The script uses the `pandas` library to read the TSV files in chunks and the `psycopg2` library to connect to the PostgreSQL database and insert the data.

### Prerequisites

Before running the script, ensure that you have the required Python libraries installed. You can install them using the following command:

```bash
pip install pandas psycopg2
```
Make sure you have a PostgreSQL database set up and update the database connection parameters in the script.
running PostgreSQL database with docker:

```bash
docker run --name imdb-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

## Usage

-    Clone the repository or download the script.

-   Update the PostgreSQL database connection parameters in the script (db_params dictionary).

-    Ensure that your PostgreSQL database is running.

-    Place the IMDb Non-Commercial Datasets TSV files in the data directory.

-    Run the script:

```bash
python import_tsv_to_postgres.py
```

## Dataset Information

The script handles the following IMDb datasets:

-    `name.basics.tsv`: Contains information about names/people.
-    `title.akas.tsv`: Contains information about alternative titles.
-    `title.basics.tsv`: Contains information about titles.
-    `title.crew.tsv`: Contains information about the crew members of titles.
-    `title.episode.tsv`: Contains information about episodes.
-    `title.principals.tsv`: Contains information about the principal cast and crew of titles.
-    `title.ratings.tsv`: Contains information about the ratings of titles.

## Configuration

The script provides a generic `import_data` function that you can easily extend to handle additional datasets. It supports parameterization for file path, table name, schema, columns, and chunk size.

## Notes

-    The script reads the TSV files in chunks to handle large datasets.
-    The default chunk size is set to 10,000, but you can adjust it based on your system's capacity.