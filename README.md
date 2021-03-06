# Just Spaces
🏕 A tool from University City District and DataMade to promote better and more just public spaces

## Requirements
- Python 3.x
- GDAL (for data imports)

## Running the app locally

1. Clone this repository and `cd` into your local copy.

    ```bash
    git clone git@github.com:datamade/just-spaces.git
    cd just-spaces
    ```

2. Create a virtual environment. (We recommend using [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) for working in a virtualized development environment.)

    ```bash
    mkvirtualenv -p python3 just-spaces
    ```

3. Install the Django requirements.

    ```bash
    pip install -r requirements.txt
    ```

4. Copy the example local settings file to the correct location:

    ```bash
    cp just-spaces/local_settings.example.py just-spaces/local_settings.py
    ```

5. Create the database:

    ```bash
    createdb just-spaces
    ```

6. Run migrations:

    ```bash
    python manage.py migrate
    ```

7. Make a superuser for so that you can access the admin interface:

    ```bash
     python manage.py createsuperuser
    ```

    Django should prompt you to provide a username, email, and password.

8. Initialize PLDP data:

    ```bash
    python manage.py initialize_pldp
    ```

9. Load ACS data:

    ```bash
    python manage.py import_data
    ```

10. Load templates:

    ```bash
    python manage.py import_survey_templates
    ```

11. Run the app locally!

    ```bash
    python manage.py runserver
    ```

    Navigate to http://localhost:8000/.

## Importing new ACS data

If you'd like to refresh ACS data, there are a few steps you'll need to take:

0. If your database is running in production, [make a backup of it with `pg_dump`](https://www.postgresql.org/docs/9.1/backup.html) just in case
1. Follow [the instructions in the `data` repo](./data/README.md#updating-data-for-a-new-year) to remake ACS data for a new year
2. Rerun `python manage.py import_data`

The `import_data` management command will update data if it already exists, so you shouldn't experience data loss during import. Still, we recommend that you practice caution and make a backup.

Since `import_data` can take a long time to finish, you can pass in flags that will tell it to only run certain parts of the data import pipeline. These flags follow the format `--${entity}-only` (e.g. `--blockgroups-only`). These flags can be useful if, for example, you're only actively developing one part of the import pipeline (like the Census block group import) and you don't want to have to wait for the rest of the job to finish in order to test your work. For full documentation of the available flags, run `./manage.py import_data --help`.

## Permissioning

This app employs three classes of users:

1. `Field users` can run published surveys.
2. `Staff users` have all the permissions of field users. They can also create, edit, and delete Agencies, Studies, Study Areas, Surveys, and Locations. They can publish surveys so they can be run by field users. Staff users can also view all collected data and design data visualizations on the collected data pages.
3. `Superusers` have all the permissions of staff users. They can also create, edit, and delete other users. Only superusers can set and change user passwords. **All superusers should also have staff status.**

In addition, list views for entities like Studies, Surveys, and CensusAreas will provide filtered results based on the Agency assigned to the current user. If a user has no Agency assigned, the user will see unfiltered results for the entity in question. This can be useful to provide users with full visibility over all entities in the system.

## On form building
This app uses a custom fork of [django-fobi](https://github.com/datamade/django-fobi) for the Create Survey, Edit Survey, and Run Survey views. django-fobi's [documentation](https://django-fobi.readthedocs.io/en/0.13.8/) is an immensely helpful resource. Add-ons to the base are in this repo's `fobi-custom` folder, including custom plugins that draw from [`django-pldp`](https://github.com/datamade/django-pldp), our implementation of the Public Life Data Protocol.
