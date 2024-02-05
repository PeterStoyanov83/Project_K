# Project K Overview

Project K is a Django-based project focused on data management and administrative control. It includes two primary
Django apps for different functionalities.

## 31.01.24 - Initialising the project 

After the research a new repository was open. 

[here is the link to the research](https://github.com/PeterStoyanov83/research_for_project_K) 

### Django Project Setup

- Initialized Django project "Project K".
- Created two apps within the project:
    - `clients`: Manages client information and functionalities.
    - `admins`: Handles administrative roles and permissions.

### Clients App - Model Definitions

- Developed models in `clients` app for:
    - Client information including ID, Name, and Location.
    - Detailed course information with sub-menu options.
    - File uploads for evaluations, feedback, billing, etc.

### PostgreSQL Database Setup

- Configured a Docker-based PostgreSQL database:
    - Database name: `Keibitz`
    - Password: `pass`

### Django Migrations

- Conducted Django migrations to set up the database schema according to defined models.

### Resolving System Check Errors

- Addressed various system check errors related to model fields and admin configurations.

### Admins App Setup

- Reconstructed `admins` app for simplified management:
    - Defined a single admin role with complete access to the database.
    - Streamlined the admin setup for ease of use and maintenance.

### Superuser Creation

- Successfully created a superuser for administrative access to the Django admin site.


### Testing the Data Functionality

- Creating a Python script that populates the database with dummy data to test the functionality and representation for the end user.
- The script is implemented as a command in the 'clients' app. It can be run using the command `python manage.py populate_data`.

