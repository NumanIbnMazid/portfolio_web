# Django Starter Template

## Description

Django Starter is a simple Skeleton to start with a Django project.

## Features

- [x] Easy Installation
- [x] Standard Project Structure
- [x] Example Landing Page using Bootstrap 5
- [x] Caching Support
- [ ] Setup script
- [x] Dockerized
- [x] Management Commands
- [ ] I18N Support

## Installation

### Requirements

(click each one for install guide)

- [Python 3.8.x](http://docs.python-guide.org/en/latest/starting/installation/)
- [pip](https://pip.pypa.io/en/stable/installation/) or [poetry](https://python-poetry.org/docs/#installation)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [docker](https://docs.docker.com/engine/install/) (optional)
- [docker-compose](https://docs.docker.com/compose/install/) (optional)

### Setup Process

### Installation Methods

1. [Using Treditional Approach](#1-using-traditional-approach)
2. [Using Docker](#2-using-docker)

#### 1. Using Traditional Approach

1. Clone the git: `git clone https://github.com/NumanIbnMazid/django_starter.git`
2. Go into the new directory: `cd django_starter`
3. Install the required dependencies.

   - Install Dependencies Using Pip

        * Run `pip install -r requirements.txt`, this will install all the required dependencies.

            Please choose to (w)ipe if asked for this:

            ````
            The plan is to install the git repository https://github.com/xxxx
            What to do?  (i)gnore, (w)ipe, (b)ackup
            ````

   - Install Dependencies Using Poetry

        * Run `poetry install`, this will install all the required dependencies.

    ```diff
    ![N:B: Replace `python` with `poetry run python` if using poetry. For example: `poetry run python manage.py runserver`]
    ```
4. Create a `.env` file and provide required environment variables using the template `.env.example` or run `python utils/generate_env.py` to automatically generate the `.env` file.
5. Run `python manage.py makemigrations` and `python manage.py migrate`, this will create the database tables
6. Run `python manage.py collectstatic`, this will collect all static files
7. Run `python manage.py runserver`
    this should start the project on port 8000.
8. Open the app on browser by navigating the url `http://127.0.0.1:8000`

- Optional: Create Django Superuser with management command `python manage.py initiate_admin`
- Optional: Configure site information with management command `python manage.py initiate_site`

#### 2. Using Docker

1. Clone the git: `git clone https://github.com/NumanIbnMazid/django_starter.git`
2. Go into the new directory: `cd django_starter`
3. Create a `.env` file and provide required environment variables using the template `.env.example`. Django SECRET_KEY can be generated from [djecrety.ir](https://djecrety.ir/)
4. Run command `docker-compose up` to start the project.
5. Open the app on browser by navigating the url `http://localhost:8000`

## Author

- [Numan Ibn Mazid](https://github.com/NumanIbnMazid)
