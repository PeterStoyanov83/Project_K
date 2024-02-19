# Project K - Django Admin Configuration

## ClientFileInline

This inline admin interface is for the `ClientFile` model. It includes a link to the file.

## ResourceInline

This inline admin interface is for the `Resource` model.

## CourseInline

This inline admin interface is for the `Course` model, specifically for the many-to-many relationship with the `Client`
model.

## ScheduleEntryInline

This inline admin interface is for the `ScheduleEntry` model.

## CourseScheduleEntryInline

This inline admin interface is for the `CourseScheduleEntry` model.

## CourseAdmin

This admin interface is for the `Course` model. It includes a list display for the `name`, `platform`, `start_date`,
and `end_date` fields, and an inline interface for the `ScheduleEntry` model.

## ScheduleEntryAdmin

This admin interface is for the `ScheduleEntry` model. It includes a list display for the course and time slots, and a
fieldset for the course and time slots. It also includes a method for checking for scheduling conflicts.

## ClientAdmin

This admin interface is for the `Client` model. It includes a list display for
the `name`, `location`, `date_of_entry`, `date_of_exit`, and `signed_agreement` fields, and inline interfaces for
the `ClientFile`, `Resource`, and `Course` models.

## CourseScheduleAdmin

This admin interface is for the `CourseSchedule` model. It includes a list display for the course and schedule.

## ResourceAdmin

This admin interface is for the `Resource` model. It includes a list display for the `seat_number`, `course`,
and `client` fields.

## LaptopAdmin

This admin interface is for the `Laptop` model. It includes a list display for
the `name`, `assigned_to`, `period_start`, and `period_end` fields.

## NotificationAdmin

This admin interface is for the `Notification` model. It includes a list display for the `user`, `message`, `read`,
and `created_at` fields.