# Project K - Setup and Running Guide

## Prerequisites
Before you start, make sure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- virtualenv (optional, but recommended)

## Setup
1. Clone the repository to your local machine.
    ```
    git clone <repository_url>
    ```
2. Navigate to the project directory.
    ```
    cd Project_K
    ```
3. (Optional) Create a virtual environment and activate it.
    ```
    virtualenv venv
    source venv/bin/activate
    ```
4. Install the required Python packages.
    ```
    pip install -r requirements.txt
    ```
5. Apply the database migrations.
    ```
    python manage.py migrate
    ```

## Running the Project
1. Start the Django development server.
    ```
    python manage.py runserver
    ```
2. Open your web browser and navigate to `http://localhost:8000`.

And that's it! You should now see the Project K homepage.

## Stopping the Project
1. To stop the Django development server, press `CTRL+C` in your terminal.
2. (Optional) If you're using a virtual environment, deactivate it.
    ```
    deactivate
    ```