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
for download and install, Save `download_and_install.sh`script and then run it in your terminal:
```bash
bash download_and_install.sh
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


## ERD
An entity-relationship diagram (ERD) for these datasets involves representing how the various data elements or entities relate to each other. Below is a verbal description of how you could design the ERD for the datasets provided:

1. **Entity:** `title.akas`
   - **Attributes:** `titleId`, `ordering`, `title`, `region`, `language`, `types`, `attributes`, `isOriginalTitle`
   - **Primary Key:** Composite key (`titleId`, `ordering`)
   - **Foreign Key:** None explicitly mentioned; `titleId` relates to `tconst` in other tables

2. **Entity:** `title.basics`
   - **Attributes:** `tconst`, `titleType`, `primaryTitle`, `originalTitle`, `isAdult`, `startYear`, `endYear`, `runtimeMinutes`, `genres`
   - **Primary Key:** `tconst`
   - **Foreign Key:** `tconst` relates to `titleId` in `title.akas`, `title.crew`, `title.episode`, `title.principals`, and `title.ratings`

3. **Entity:** `title.crew`
   - **Attributes:** `tconst`, `directors`, `writers`
   - **Primary Key:** `tconst`
   - **Foreign Key:** `tconst` relates to `titleId` in `title.akas` and `tconst` in `title.basics`

4. **Entity:** `title.episode`
   - **Attributes:** `tconst`, `parentTconst`, `seasonNumber`, `episodeNumber`
   - **Primary Key:** `tconst`
   - **Foreign Key:** `parentTconst` relates to `tconst` of the `title.basics` entity

5. **Entity:** `title.principals`
   - **Attributes:** `tconst`, `ordering`, `nconst`, `category`, `job`, `characters`
   - **Primary Key:** Composite key (`tconst`, `ordering`)
   - **Foreign Key:** `tconst` relates to `titleId` in `title.akas` and `tconst` in `title.basics`; `nconst` relates to `name.basics`

6. **Entity:** `title.ratings`
   - **Attributes:** `tconst`, `averageRating`, `numVotes`
   - **Primary Key:** `tconst`
   - **Foreign Key:** `tconst` relates to `titleId` in `title.akas` and `tconst` in `title.basics`

7. **Entity:** `name.basics`
   - **Attributes:** `nconst`, `primaryName`, `birthYear`, `deathYear`, `primaryProfession`, `knownForTitles`
   - **Primary Key:** `nconst`
   - **Foreign Key:** `nconst` relates to `nconst` in `title.principals`

Now, to tie this together visually in an ERD, you could depict each entity as a box and draw lines representing the relationships between them, usually with some kind of notation at the ends of the lines indicating the nature of the relationship (one-to-many, many-to-many, etc.).

## Notes

-    The script reads the TSV files in chunks to handle large datasets.
-    The default chunk size is set to 10,000, but you can adjust it based on your system's capacity.