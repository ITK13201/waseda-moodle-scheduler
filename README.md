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
pipenv run update
```

### Notify the calendar information just before the deadline.

```shell
pipenv run notify
```

### Tracking and Format "*.py" file

```shell
pipenv run watch
```

### Format changed "*.py" file

```shell
pipenv run format
```
