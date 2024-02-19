# Project K - Django Forms Documentation

## ClientFileForm

The `ClientFileForm` is a model form for the `ClientFile` model. It only includes the `file` field.

## ResourceForm

The `ResourceForm` is a model form for the `Resource` model. It includes all fields from the model. The `seat_number`
field uses a custom select widget and is optional.

## LaptopForm

The `LaptopForm` is a model form for the `Laptop` model. It includes all fields from the model.

## ClientForm

The `ClientForm` is a model form for the `Client` model. It includes
the `name`, `location`, `date_of_entry`, `date_of_exit`, and `signed_agreement` fields.

## CourseForm

The `CourseForm` is a model form for the `Course` model. It includes
the `name`, `description`, `platform`, `start_date`, `end_date`, and `clients` fields.