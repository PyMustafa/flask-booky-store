# flask-booky-store

## Setup Instructions

### Using Poetry

1. Install Poetry if you haven't already:
   ```sh
   # For Linux/MacOS
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   For Windows users, you can follow the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation).

2. Create & activate virtual environment.
   Using poetry shell (the easiest way)
    - Install the Shell Plugin
        ```sh
        poetry self add poetry-plugin-shell
        ```
    - Activate the virtual environment.
        ```sh
        poetry shell
        ```

3. Install the project dependencies using Poetry:
   ```sh
   poetry install
   ```

### Using Python venv

1. Create a virtual environment:
   ```sh
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Linux/MacOS:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```

3. Install the project dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Start the Server

Start the server:
   ```sh
   flask run --debug
   ```
