# Advanote

## About The Project

It's app for writing task, notes, projects when you team can work!

## Getting Started

For work the project need download project files.
Go to you work path and use this commands in console:

### Download Project Files

```commandline
git clone https://gitlab.crja72.ru/django_2023/projects/team11.git
```

### Venv Installation And Activation

For more comfortable work in your project create venv:

```commandline
python -m venv venv
```

For activation venv use this command:

```commandline
For windows:
venv\Scripts\activate
For Linux/MacOs:
source venv/bin/activate
```

### Requirements

For correctly work project need install requirements:

1. Install prod requirements:
    ```commandline 
    pip install -r requirements/prod.txt
    ```
2. Install test requirements:
    ```commandline 
    pip install -r requirements/test.txt
    ```
3. Install dev requirements:
   ```commandline 
    pip install -r requirements/dev.txt
   ```
If you want download all requirements in one command just use:
```commandline
pip install -r requirements/requirements.txt
```

## Start dev-mode

For run dev-mode use this command:

```commandline
cd advanote

python manage.py runserver
```

If everything worked correctly, you will receive a message like this

```commandline
Starting development server at http://127.0.0.1:8000/
```

## Test run

If you want check project work correctly run tests.
For run tests use this command:

```commandline
python advanote/manage.py test
```

## Load Fixtures
For loading fixtures data use this command:
```commandline
python manage.py loaddata fixtures/data.json
```
## Dump Fixtures
For dumping data fixtures use this command:
```commandline
python -Xutf8 manage.py dumpdata catalog -o fixtures/data.json
```

## Migrations
When making changes to the database schema, you need to create and apply migrations. Use the following commands:

```commandline
python manage.py makemigrations
python manage.py migrate
```

## Contacts

Ruslan - [Telegram](https://t.me/rs31113)
