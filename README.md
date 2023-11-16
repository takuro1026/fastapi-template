# fastapi-template

This is a straightforward service template built with FastAPI, primarily designed for personal use. 
However, feel free to explore it if it suits your needs.

## Prerequisite:
1. Utilize Python 3.11 (Feel free to adjust the version as per your requirements).
2. Make sure you have installed [pip](https://pip.pypa.io/en/stable/) or [poetry](https://python-poetry.org/)

## Run for Dev
1. Clone this repo through following command
    ```
    git clone https://github.com/takuro1026/fastapi-template
    ```
2. Install dependencies by pip or poetry. (Highly recommend to create a virtual environment instead of installing locally)
    ```
    // Install via pip
    pip install -r requirements.txt
   
    // Install via Poetry
    poetry shell
    poetry install
    ```
3. Run the service locally
    ```
    uvicorn app.main:app --reload --log-config=./app/config/log_config.yaml
    ```
4. You can find API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Export package info to requirements.txt from pyproject.toml
```
poetry export -f requirements.txt --output requirements.txt
```