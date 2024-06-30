# Forex Trading Platform API

## Goal
    
    Implement an API to simulate a simple trading platform

## Features

- Place orders
- Retrieve all orders with pagination
- Retrieve specific orders by ID
- Cancel (delete) orders

## Requirements

- Python 3.8+
- FastAPI
- SQLModel
- SQLAlchemy
- FastAPI Pagination
- AsyncIO
- Pydantic


## Execution

The decision of whether to create a virtual env for executing the script is up to the user. In my case, I've created a virtual env, but I haven't committed it.

To run the API:

    fastapi dev main.py


## Project Structure

The project was organized following the typical structure of a python package project, that's the reason to include a *setup.py* file.

To compile the package, execute the following command:

    python setup.py sdist bdist_wheel

this command generates a wheel and a tarball (.tar.gz) file of the version configured on the *setup.py*

## To Do

Next steps:

- create logs
- create unit tests
- create docker container
- create websocket