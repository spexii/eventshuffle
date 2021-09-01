# eventshuffle

Simple event scheduling application. Users can create events with dates and vote for suitable dates.

## Running the application

The project can be run on your local machine either by having pipenv installed or by having Docker installed.

### Pipenv

**Prerequisites:** Pipenv is installed

1. Download project codes to some directory on your local machine, let's say for example `~/dev/eventshuffle`

2. Run the following commands

```
$ cd ~/dev/eventshuffle
$ pipenv shell
$ ./manage.py migrate
$ ./manage.py runserver
```

Now the application is running and API can be found at http://127.0.0.1:8000/api/v1/
