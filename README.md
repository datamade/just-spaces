# Just Spaces
🏕 A tool from DataMade and University City District to promote better and more just public spaces

## Requirements
- Python 3.x
- Docker

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
    pip install -r requirements.txt -r dev-requirements.txt
    ```

4. Copy the example local settings file to the correct location:

    ```bash
    cp just-spaces/local_settings.example.py just-spaces/local_settings.py
    ```

5. Install NPM dependencies for the frontend:

    ```bash
    docker-compose build
    ```

6. Create the database:

    ```bash
    createdb just-spaces
    ```

7. Run migrations:

    ```bash
    python manage.py migrate
    ```

8. Make a superuser for so that you can access the admin interface:

    ```bash
     python manage.py createsuperuser
    ```

    Django should prompt you to provide a username, email, and password.

9. Run the app locally!

    ```bash
    # In one shell, bundle and watch JavaScript assets
    docker-compose up

    # In another shell, run the dev server
    python manage.py runserver
    ```

    Navigate to http://localhost:8000/.

## On form building
This app uses a custom fork of [django-fobi](https://github.com/datamade/django-fobi) for the Create Survey, Edit Survey, and Run Survey views. django-fobi's [documentation](https://django-fobi.readthedocs.io/en/0.13.8/) is an immensely helpful resource. Add-ons to the base are in this repo's `fobi-custom` folder, including custom plugins that draw from [`django-pldp`](https://github.com/datamade/django-pldp), our implementation of the Public Life Data Protocol. 
