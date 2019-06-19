# Just Spaces Data Collection

## Requirements

- Docker
- Docker Compose

## Installation

Sign up for a Census API key here: https://api.census.gov/data/key_signup.html
Then, create an `.env` file:

```bash
# Edit this file to add your Census API key
cp .env.example .env
```

Alternatively, if you're indoctrinated into this project, retrieve the canonical
`.env` file from the Blackbox keyring:

```
blackbox_cat ../configs/.env.gpg > .env
```

Next, install requirements with Docker Compose:

```
docker-compose build
```

## Making data

Make the data:

```
docker-compose run --rm make
```

To remove generated files to rerun the pipeline:

```
docker-compose run --rm make clean
```

## Updating data for a new year

If you'd like to update ACS data for a new year, you'll need to remove the generated files and rerun the Make pipeline.

Start by removing generated files:

```
docker-compose run --rm make clean
```

Next, adjust the global variable `YEAR` in `Makefile` to correspond to the year you'd like to retrieve ACS estimates for.

Finally, rerun the pipeline with `docker-compose run --rm make`. This will create new files in the `data` directory that you can use to import into the app.
