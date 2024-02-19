
# Django Command Line Utilities

## Starting a New Project
To start a new Django project, use the `startproject` command.
```bash
django-admin startproject projectname
```

## Starting a New App
To start a new app within your Django project, use the `startapp` command.
```bash
python manage.py startapp appname
```

## Running the Development Server
To start the Django development server, use the `runserver` command.
```bash
python manage.py runserver
```

## Creating Database Migrations
To create new migrations based on the changes you've made to your models, use the `makemigrations` command.
```bash
python manage.py makemigrations
```

## Applying Database Migrations
To apply existing migrations and update your database schema, use the `migrate` command.
```bash
python manage.py migrate
```

## Creating a Superuser
To create a new superuser for the Django admin interface, use the `createsuperuser` command.
```bash
python manage.py createsuperuser
```

## Running Tests
To run your Django tests, use the `test` command.
```bash
python manage.py test
```

## Collecting Static Files
To collect all your static files into the `STATIC_ROOT` directory, use the `collectstatic` command.
```bash
python manage.py collectstatic
```

## Checking for Problems
To check your project for common problems, use the `check` command.
```bash
python manage.py check
```

## Interactive Python Shell
To start an interactive Python shell with your Django settings, use the `shell` command.
```bash
python manage.py shell
```

And there you have it, a quick guide to the most popular Django command line utilities. Ready to be served in your README.md file. Enjoy!
```