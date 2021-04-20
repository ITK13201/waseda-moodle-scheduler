# Waseda Moodle Scheduler

This is an application that receives the calendar information on Waseda moodle as an ics file and notifies the discord of it.

## Install

```shell
pip install pipenv
pipenv install --dev
```

## Usage

### Enter the virtual environment

```shell
pipenv shell
```

### Update the calendar information and send a notification

```shell
python manage.py update_events_data
```

### Format "*.py" file automatically

```shell
pipenv run watch
```
