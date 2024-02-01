# Project K Overview

Project K is a Django-based project focused on data management and administrative control. It includes two primary
Django apps for different functionalities.

## Day 1 Progress

### Step 1: Django Project Setup

- Initialized Django project "Project K".
- Created two apps within the project:
    - `clients`: Manages client information and functionalities.
    - `admins`: Handles administrative roles and permissions.

### Step 2: Clients App - Model Definitions

- Developed models in `clients` app for:
    - Client information including ID, Name, and Location.
    - Detailed course information with sub-menu options.
    - File uploads for evaluations, feedback, billing, etc.

### Step 3: PostgreSQL Database Setup

- Configured a Docker-based PostgreSQL database:
    - Database name: `Keibitz`
    - Password: `pass`

### Step 4: Django Migrations

- Conducted Django migrations to set up the database schema according to defined models.

### Step 5: Resolving System Check Errors

- Addressed various system check errors related to model fields and admin configurations.

### Step 6: Admins App Setup

- Reconstructed `admins` app for simplified management:
    - Defined a single admin role with complete access to the database.
    - Streamlined the admin setup for ease of use and maintenance.

### Step 7: Superuser Creation

- Successfully created a superuser for administrative access to the Django admin site.
