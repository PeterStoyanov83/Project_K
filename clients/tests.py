from django.test import TestCase
from clients.models import Client, Course, CourseSchedule, ClientFile, Resource, Laptop
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date


class ClientModelTest(TestCase):

    def test_create_client(self):
        client = Client.objects.create(
            name="John Doe",
            location="office",
            date_of_entry=date.today(),
            signed_agreement=True
        )
        self.assertEqual(client.name, "John Doe")
        self.assertTrue(client.signed_agreement)


class CourseModelTest(TestCase):

    def test_create_course(self):
        course = Course.objects.create(
            name="Python Development",
            platform="online"
        )
        self.assertEqual(course.name, "Python Development")
        self.assertEqual(course.platform, "online")


class CourseScheduleModelTest(TestCase):

    def test_create_course_schedule(self):
        course = Course.objects.create(name="Python Development", platform="online")
        schedule = CourseSchedule.objects.create(
            course=course,
            day_of_week="Monday",
            time_slot="08:30-10:00"
        )
        self.assertEqual(schedule.day_of_week, "Monday")
        self.assertIn(schedule, course.courseschedule_set.all())


class ClientFileModelTest(TestCase):

    def test_create_client_file(self):
        client = Client.objects.create(name="John Doe", location="office")
        client_file = ClientFile.objects.create(
            client=client,
            file=SimpleUploadedFile("test_file.pdf", b"these are the file contents!")
        )
        self.assertEqual(client_file.client, client)
        self.assertTrue(client_file.file.name.endswith('.pdf'))


class ResourceModelTest(TestCase):

    def test_create_resource(self):
        client = Client.objects.create(name="John Doe", location="office")
        course = Course.objects.create(name="Python Development", platform="online")
        resource = Resource.objects.create(
            room="room_1",
            seat_number="1",
            course=course,
            client=client
        )
        self.assertEqual(resource.room, "room_1")
        self.assertEqual(resource.client, client)
        self.assertEqual(resource.course, course)


class LaptopModelTest(TestCase):

    def test_create_laptop(self):
        laptop = Laptop.objects.create(
            name="Laptop 1",
            period_start=date.today(),
            period_end=date.today()
        )
        self.assertEqual(laptop.name, "Laptop 1")
        self.assertEqual(laptop.period_start, date.today())

    def test_assign_laptop_to_client(self):
        client = Client.objects.create(name="John Doe", location="office")
        laptop = Laptop.objects.create(
            name="Laptop 1",
            period_start=date.today(),
            period_end=date.today(),
            assigned_to=client
        )
        self.assertEqual(laptop.assigned_to, client)
