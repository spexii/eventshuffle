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
$ pipenv install
$ ./manage.py migrate
$ ./manage.py runserver
```

Now the application is running and API can be found at http://127.0.0.1:8000/api/v1/.

**What did the commands do?** pipenv shell spawns a virtual environment that has everything installed that the project needs. After that all packages are installed that are needed for the project. Packages can be also installed with -d option, when also the develop environment packages are installed. manage.py is Django's command-line utility, that is used here to run database migrations and finally to run the simple testing web server.

### Docker

**Prerequisites:** Docker and docker-compose are installed

1. Download project codes to some directory on your local machine, let's say for example `~/dev/eventshuffle`

2. Run the following commands

```
$ cd ~/dev/eventshuffle/docker
$ docker-compose --project-name eventshuffle up
```

Now the application is running and API can be found at http://127.0.0.1:8000/api/v1/

**What did the commands do?** The docker container is started up with docker-compose, and that container has everything the project needs. Migrations have been already run and the project is ready to use by just starting it up.
