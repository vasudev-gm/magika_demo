# Magika Demo using minimal Django Ninja APIs

## Badges

[![Dependabot Updates](https://github.com/vasudev-gm/magika_demo/actions/workflows/dependabot/dependabot-updates/badge.svg?branch=master)](https://github.com/vasudev-gm/magika_demo/actions/workflows/dependabot/dependabot-updates)

> **Magika** is Google's ML based File type Detection model in near constant inference time regardless of file sizes.
Utilizes upload api in swagger to return detected File Type. Supports Python 3.9+. Works on Linux, Windows and Mac.\
[Magika File Type Checker by Google](https://github.com/google/magika)
---

## API Documentation
>
> You can find the api documentation or openAPI docs at `http://127.0.0.1/api/docs`
---

## Python Environment Setup (Local System)
>
> You can create an isolated virtual environment using Python 3.13 and install packages using pip
or pipenv or uv.

## UV commands to setup environment and run the project

> uv venv -p 3.13 --python-preference managed
> uv sync

## UV command to upgrade python and packages

> uv python upgrade
> uv sync --upgrade

## UV export to requirements.txt

> uv export --format=requirements.txt --all-packages > .\requirements.txt

## How To Run the project (Local System)
>
> cd example\
> python manage.py runserver\
***You can Ignore migration not applied warnings after running runserver***

## Running the project using Docker

Deployed using Granian Server instead of Gunicorn

## Docker Compose Commands

Get running containers

`docker ps`

Build and Run in detached mode

`docker compose up --build -d`

To enter Bash Shell for migrating db changes or static files

`docker exec -it <container id from docker ps> bash`

To view logs of container. You can pass head to view first N lines or tail to view last N lines specified by argument after head/tail

`docker logs --tail 1000 -f <container id from docker ps>`

---

## Acknowledgement

@software{magika,
author = {Fratantonio, Yanick and Bursztein, Elie and Invernizzi, Luca and Zhang, Marina and Metitieri, Giancarlo and Kurt, Thomas and Galilee, Francois and Petit-Bianco, Alexandre and Farah, Loua and Albertini, Ange},
title = {{Magika content-type scanner}},
url = {<https://github.com/google/magika>}
}
