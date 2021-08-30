#!/bin/bash

# Run migrations just before starting the web server
su - eventsfl -c "cd /webapp/eventshuffle && pipenv run python manage.py migrate"
