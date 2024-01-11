# Advanote

## About The Project

This project aims to develop a collaborative web application for advanced note-taking, facilitating seamless sharing and editing of notes among teams. The application is designed to empower users to create, edit, and collaboratively utilize notes, fostering team efficiency, productivity, and streamlined information exchange.

## Getting Started

To start working on the project, you'll need to download the project files. 
Navigate to your working directory and execute the following commands in the console.

### Download Project Files

```commandline
git clone https://github.com/rs31113/Advanote.git
```

### Venv Installation And Activation

To enhance your project workflow, create a virtual environment (venv).

```commandline
python -m venv venv
```

To activate your venv use this command.

```commandline
For windows:
venv\Scripts\activate
For Linux/MacOs:
source venv/bin/activate
```

### Requirements

For the project to function properly, it's necessary to install the required dependencies.

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
You can install all requirements using one command.
```commandline
pip install -r requirements/requirements.txt
```

## Start dev-mode

To run dev-mode use this command.

```commandline
cd advanote

python manage.py runserver
```

If everything worked correctly, you will receive a message like this.

```commandline
Starting development server at http://127.0.0.1:8000/
```

## Test run

To ensure the project operates correctly, run tests. 
Execute the following command to run the tests.

```commandline
python advanote/manage.py test
```

## Load Fixtures
To load fixture data, utilize this command.
```commandline
python manage.py loaddata fixtures/data.json
```
## Dump Fixtures
To export fixture data, employ this command.
```commandline
python -Xutf8 manage.py dumpdata catalog -o fixtures/data.json
```

## Migrations
To update the database structure, it's essential to generate and implement migrations. 
Employ the commands below.

```commandline
python manage.py makemigrations
python manage.py migrate
```

## Contacts

Ruslan Shafikov - [Telegram](https://t.me/rs31113)
