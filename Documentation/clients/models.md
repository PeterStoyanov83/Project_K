# Project K - Django Models Documentation

## Client Model
The `Client` model represents a client in the system. Each client has the following fields:
- `name`: A string representing the client's name.
- `location`: A string representing the client's location.
- `date_of_entry`: A date marking the client's entry.
- `date_of_exit`: A date marking the client's exit. This field is optional.
- `signed_agreement`: A boolean indicating whether the client has signed an agreement.
- `assigned_laptop`: A foreign key to a `Laptop` model. This field is optional.

## Course Model
The `Course` model represents a course in the system. Each course has the following fields:
- `name`: A string representing the course's name.
- `description`: A text field representing the course's description.
- `platform`: A string representing the course's platform.
- `other_platform_comment`: A text field for additional comments about the platform. This field is optional.
- `start_date`: A date marking the start of the course.
- `end_date`: A date marking the end of the course.
- `clients`: A many-to-many relationship with the `Client` model.

## Scheduling Models
The scheduling system is represented by several models: `DayOfWeek`, `TimeSlot`, `ScheduleEntry`, `CourseSchedule`, and `CourseScheduleEntry`. These models work together to create a complex scheduling system for the courses.

## ClientFile Model
The `ClientFile` model represents a file uploaded by a client. Each file has the following fields:
- `client`: A foreign key to the `Client` model.
- `file`: A file field for the uploaded file.
- `uploaded_at`: A datetime marking when the file was uploaded.

## Resource Model
The `Resource` model represents a seat in a course. Each resource has the following fields:
- `seat_number`: A string representing the seat number.
- `course`: A foreign key to the `Course` model. This field is optional.
- `client`: A foreign key to the `Client` model. This field is optional.

## Laptop Model
The `Laptop` model represents a laptop that can be assigned to a client. Each laptop has the following fields:
- `name`: A string representing the laptop's name.
- `assigned_to`: A foreign key to the `Client` model. This field is optional.
- `period_start`: A date marking the start of the assignment period.
- `period_end`: A date marking the end of the assignment period.
- `comments`: A text field for additional comments. This field is optional.

## Notification Model
The `Notification` model represents a message sent to a user. Each notification has the following fields:
- `user`: A foreign key to the `User` model.
- `message`: A text field for the message.
- `read`: A boolean indicating whether the notification has been read.
- `created_at`: A datetime marking when the notification was created.