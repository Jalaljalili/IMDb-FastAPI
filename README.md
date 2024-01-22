# IMDb Non-Commercial Datasets Import to PostgreSQL

This Python script is designed to import IMDb Non-Commercial Datasets into a PostgreSQL database. It utilizes SQLAlchemy ORM for defining table structures and Pandas for data manipulation.

## Prerequisites

Make sure you have the following prerequisites installed:

- Python
- PostgreSQL
- Pandas
- SQLAlchemy

You can install Python dependencies using the following command:

```bash
pip install pandas sqlalchemy
```
## Usage

1. Set PostgreSQL Database Connection Parameters

    Update the db_params dictionary with your PostgreSQL database connection parameters (host, port, database, user, password).

2.    Run the Script

    Execute the script using the following command:
    ```shell
    python import_data.py

    ```
 3.    Review Import Errors

    If there are errors during data import, the script will log them in separate files named table_name_import_errors.log.

## Tables and Relationships

#### The script defines the following tables using SQLAlchemy ORM:

    NameBasics:
        nconst (PK)
        primaryName
        birthYear
        deathYear
        primaryProfession
        knownForTitles

    TitleAkas:
        titleId (PK)
        ordering (PK)
        title
        region
        language
        types
        attributes
        isOriginalTitle

    TitleBasics:
        tconst (PK)
        titleType
        primaryTitle
        originalTitle
        isAdult
        startYear
        endYear
        runtimeMinutes
        genres

    TitleCrew:
        tconst (PK, FK)
        directors
        writers

    TitleEpisode:
        tconst (PK, FK)
        parentTconst (FK)
        seasonNumber
        episodeNumber

    TitlePrincipals:
        tconst (PK, FK)
        ordering (PK)
        nconst
        category
        job
        characters

    TitleRatings:
        tconst (PK, FK)
        averageRating
        numVotes

#### Additional Notes

-    The script creates the IMDB database if it does not exist.
-    Data import errors are logged for review.
-    Tables are defined with relationships based on foreign key constraints.

Feel free to customize the script and table structures based on your specific needs.

Note: Ensure you have the necessary permissions and have backed up your data before running the script.   Review Import Errors

    If there are errors during data import, the script will log them in separate files named table_name_import_errors.log.

Tables and Relationships

The script defines the following tables using SQLAlchemy ORM:

    NameBasics:
        nconst (PK)
        primaryName
        birthYear
        deathYear
        primaryProfession
        knownForTitles

    TitleAkas:
        titleId (PK)
        ordering (PK)
        title
        region
        language
        types
        attributes
        isOriginalTitle

    TitleBasics:
        tconst (PK)
        titleType
        primaryTitle
        originalTitle
        isAdult
        startYear
        endYear
        runtimeMinutes
        genres

    TitleCrew:
        tconst (PK, FK)
        directors
        writers

    TitleEpisode:
        tconst (PK, FK)
        parentTconst (FK)
        seasonNumber
        episodeNumber

    TitlePrincipals:
        tconst (PK, FK)
        ordering (PK)
        nconst
        category
        job
        characters

    TitleRatings:
        tconst (PK, FK)
        averageRating
        numVotes

Additional Notes

    The script creates the IMDB database if it does not exist.
    Data import errors are logged for review.
    Tables are defined with relationships based on foreign key constraints.

Feel free to customize the script and table structures based on your specific needs.

#### Note: Ensure you have the necessary permissions and have backed up your data before running the script.