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

Remove generated files to rerun the pipeline:

```
docker-compose run --rm make clean
```
