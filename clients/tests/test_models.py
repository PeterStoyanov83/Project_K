from django.test import TestCase
from datetime import date, timedelta
from clients.models import Course, DayOfWeek, CourseSchedule


class CourseScheduleModelTest(TestCase):

    def setUp(self):
        # Create test course and day of week
        self.course = Course.objects.create(
            name="Test Course",
            platform="online",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        self.day = DayOfWeek.objects.create(name="Monday")
        # Create a CourseSchedule instance
        self.course_schedule = CourseSchedule.objects.create(course=self.course)
        self.course_schedule.days.add(self.day)

    def test_string_representation(self):
        """
        Test if the string representation of the CourseSchedule
        contains the name of the days assigned to it.
        """
        self.assertIn("Monday", str(self.course_schedule))

    def test_course_schedule_creation(self):
        """
        Test if a CourseSchedule can be created with valid data.
        """
        self.assertEqual(self.course_schedule.course, self.course)

    def test_course_schedule_days(self):
        """
        Test if days can be added to a CourseSchedule.
        """
        self.assertEqual(self.course_schedule.days.count(), 1)
        self.assertIn(self.day, self.course_schedule.days.all())

    def test_course_schedule_overlap(self):
        """
        Test if CourseSchedules can overlap in time.
        """
        # Create another course with overlapping time period
        overlapping_course = Course.objects.create(
            name="Overlapping Course",
            platform="online",
            start_date=self.course.start_date + timedelta(days=10),
            end_date=self.course.end_date + timedelta(days=10)
        )
        overlapping_schedule = CourseSchedule.objects.create(course=overlapping_course)
        overlapping_schedule.days.add(self.day)

        # Test if overlap is detected
        self.assertTrue(self.course_schedule.overlaps_with(overlapping_schedule))

    def test_course_schedule_no_overlap(self):
        """
        Test if CourseSchedules that don't overlap return False.
        """
        # Create another course with non-overlapping time period
        non_overlapping_course = Course.objects.create(
            name="Non-overlapping Course",
            platform="online",
            start_date=self.course.end_date + timedelta(days=1),
            end_date=self.course.end_date + timedelta(days=31)
        )
        non_overlapping_schedule = CourseSchedule.objects.create(course=non_overlapping_course)
        non_overlapping_schedule.days.add(self.day)

        # Test if overlap is detected
        self.assertFalse(self.course_schedule.overlaps_with(non_overlapping_schedule))

    def test_course_schedule_str(self):
        """
        Test if the __str__ method of CourseSchedule returns
        the expected string representation.
        """
        expected_str = f"{self.course.name} Schedule"
        self.assertEqual(str(self.course_schedule), expected_str)

    # Additional test cases can be added as needed
