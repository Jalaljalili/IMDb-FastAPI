#!/bin/bash

# Create data directory
mkdir data

# Download IMDb datasets
wget https://datasets.imdbws.com/title.akas.tsv.gz -O data/title.akas.tsv.gz
wget https://datasets.imdbws.com/title.basics.tsv.gz -O data/title.basics.tsv.gz
wget https://datasets.imdbws.com/title.crew.tsv.gz -O data/title.crew.tsv.gz
wget https://datasets.imdbws.com/title.episode.tsv.gz -O data/title.episode.tsv.gz
wget https://datasets.imdbws.com/title.principals.tsv.gz -O data/title.principals.tsv.gz
wget https://datasets.imdbws.com/title.ratings.tsv.gz -O data/title.ratings.tsv.gz
wget https://datasets.imdbws.com/name.basics.tsv.gz -O data/name.basics.tsv.gz

# Extract gzipped files
gunzip data/title.akas.tsv.gz
gunzip data/title.basics.tsv.gz
gunzip data/title.crew.tsv.gz
gunzip data/title.episode.tsv.gz
gunzip data/title.principals.tsv.gz
gunzip data/title.ratings.tsv.gz
gunzip data/name.basics.tsv.gz
# Install required Python libraries
pip install pandas psycopg2

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Run PostgreSQL container
docker run --name imdb-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

echo "Docker container 'imdb-postgres' is now running with PostgreSQL. Connect using:"
echo "psql -h localhost -p 5432 -U postgres -d postgres -W"
