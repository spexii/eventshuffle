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

**What did the commands do?** The docker container is started up with docker-compose. If the image doesn't exist on your computer, it is downloaded from Docker Hub before starting up the project. The container has everything the project needs. Migrations have been already run and the project is ready to use by just starting it up.

## Usage

This project is based on this: https://gist.github.com/anttti/2b69aebc63687ebf05ec. The API can be used just like described in that link with the exception of the first section "List all events". Events can't be listed with `/api/v1/event/list`, since by default Django REST Framework offers the listing by just navigating to `/api/v1/event/`. There was no point to create another custom action for that listing.
