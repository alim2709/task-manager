# Task manager

Django project for managing projects, teams, tasks and workers in Task Manager

## Check it out

[Task Manager Deployed to Render](https://task-manager-fn50.onrender.com/)


User for testing:

```shell
username: jacob_circle
password: test123password
```

## Installation

Python3 must be already be installed!

```shell
git clone https://github.com/alim2709/task-manager.git
cd task-manager
python3 -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

Environment Variables

The following environment variables should be set in the .env file:

SECRET_KEY: Your  secret key

Note: Before starting the project, make a copy of the .env_sample file and rename it to .env. Replace the sample values with your actual environment variable values.
```shell
python manage.py migrate
python3 manage.py runserver
```

## Run the tests

```shell
python3 manage.py test
```

## Features
* Authentication functionality for Worker/User
* Managing projects, teams, tasks, task types, workers, and positions directly from the website
* Powerful admin panel for advanced management
