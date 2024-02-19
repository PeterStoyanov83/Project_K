# Project K - Data Populator

This script is a custom Django management command used to populate the database with sample data. It uses the `Faker`
library to generate fake data.

## populate_clients

This function creates `n` fake `Client` instances. Each client has a randomly
generated `name`, `location`, `date_of_entry`, `date_of_exit` (which can be `None`), and `signed_agreement`.

## populate_schedule_entries

This function creates `n` fake `ScheduleEntry` instances. Each schedule entry is associated with a random `Course` and
has a randomly generated day and time slot.

## populate_client_files

This function creates `n` fake `ClientFile` instances. Each client file is associated with a random `Client` and has a
randomly generated file name and `uploaded_at` datetime.

## populate_resources

This function creates a `Resource` instance for each `Course`. Each resource is associated with a random `Client` and
has a randomly generated `seat_number`.

## Command

This is the custom Django management command. When run, it calls the above functions to populate the database with
sample data.

```
python manage.py populate_data
```