# Magika Demo using minimal Django Ninja APIs
> **Magika** is Google's ML based File type Detection model in near constant inference time regardless of file sizes.
Utilizes upload api in swagger to return detected File Type. Supports Python 3.8 to 3.11. Works on Linux, Windows and Mac.\
[Magika File Type Checker by Google](https://github.com/google/magika)
---
## API Documentation
> You can find the api documentation or openAPI docs at `http://127.0.0.1/api/docs`
---
## Python Environment Setup
> You can create an isolated virtual environment using Python 3.11 and install packages using pip
or pipenv.\
[Python API Usage](https://pypi.org/project/magika/)

## How To Run the project
> cd example\
> python manage.py runserver\
***You can Ignore migration not applied warnings after running runserver***
---
## Acknowledgement
@software{magika,
author = {Fratantonio, Yanick and Bursztein, Elie and Invernizzi, Luca and Zhang, Marina and Metitieri, Giancarlo and Kurt, Thomas and Galilee, Francois and Petit-Bianco, Alexandre and Farah, Loua and Albertini, Ange},
title = {{Magika content-type scanner}},
url = {https://github.com/google/magika}
}