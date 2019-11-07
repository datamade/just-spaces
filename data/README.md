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
(cd .. && blackbox_cat configs/.env.gpg > data/.env)
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

## Adding a new Region

If you'd like to add a new CensusRegion, here are the steps you should follow:

1. Update `STATES` in `scripts/states.py`
    1. If the region is in a new state, create a new entry in `STATES` for that state; otherwise, update the existing state
    2. Add a region to the `regions` dictionary with the counties comprising this region, its default map zoom level, and its center coordinate
2. Add any new states to the `shapefiles` target in `shapefiles.mk`
3. Rerun the data import with `docker-compose run --rm make clean` and `docker-compose run --rm make`
