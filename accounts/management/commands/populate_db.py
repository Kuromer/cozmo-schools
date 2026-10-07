from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from school.models import Student, SchoolClass, Fee, Warning, ParentInvitation, Homework, Evaluation, Attendance, Message
from datetime import date, time, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate the database with mock data for cozmo School Management System'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        Message.objects.all().delete()
        Attendance.objects.all().delete()
        Evaluation.objects.all().delete()
        Homework.objects.all().delete()
        ParentInvitation.objects.all().delete()
        Warning.objects.all().delete()
        Fee.objects.all().delete()
        SchoolClass.objects.all().delete()
        Student.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating users...')
        # Admin
        admin_user, _ = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'System',
                'last_name': 'Admin',
                'email': 'admin@cozmo.school',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        # Teachers
        teacher1 = CustomUser.objects.create_user(
            username='mr_ahmed', password='teacher123',
            first_name='Mr.', last_name='Ahmed',
            email='ahmed.teacher@cozmo.school', role='teacher'
        )
        teacher2 = CustomUser.objects.create_user(
            username='ms_sara', password='teacher123',
            first_name='Ms.', last_name='Sara',
            email='sara.teacher@cozmo.school', role='teacher'
        )
        teacher3 = CustomUser.objects.create_user(
            username='mr_mohamed', password='teacher123',
            first_name='Mr.', last_name='Mohamed',
            email='mohamed.teacher@cozmo.school', role='teacher'
        )

        # Parents
        parent1 = CustomUser.objects.create_user(
            username='ahmed_parent', password='parent123',
            first_name='Ahmed\'s', last_name='Parent',
            email='ahmed.parent@cozmo.school', role='parent',
            phone='+1234567890'
        )
        parent2 = CustomUser.objects.create_user(
            username='omar_parent', password='parent123',
            first_name='Omar\'s', last_name='Parent',
            email='omar.parent@cozmo.school', role='parent',
            phone='+0987654321'
        )

        self.stdout.write('Creating students...')
        ahmed = Student.objects.create(first_name='Ahmed', last_name='Mohamed', parent=parent1, grade_level='Grade 5', date_of_birth=date(2015, 3, 15))
        omar = Student.objects.create(first_name='Omar', last_name='Khaled', parent=parent2, grade_level='Grade 5', date_of_birth=date(2015, 7, 22))
        mariam = Student.objects.create(first_name='Mariam', last_name='Ahmed', parent=parent1, grade_level='Grade 4', date_of_birth=date(2016, 1, 10))
        youssef = Student.objects.create(first_name='Youssef', last_name='Ali', parent=parent2, grade_level='Grade 6', date_of_birth=date(2014, 11, 5))

        self.stdout.write('Creating classes...')
        class_5a = SchoolClass.objects.create(name='Class 5A', grade_level='Grade 5')
        class_5a.teachers.add(teacher1, teacher2)
        class_5a.students.add(ahmed, omar)

        class_4a = SchoolClass.objects.create(name='Class 4A', grade_level='Grade 4')
        class_4a.teachers.add(teacher2)
        class_4a.students.add(mariam)

        class_6a = SchoolClass.objects.create(name='Class 6A', grade_level='Grade 6')
        class_6a.teachers.add(teacher3)
        class_6a.students.add(youssef)

        self.stdout.write('Creating fees...')
        today = date.today()
        Fee.objects.create(student=ahmed, amount=Decimal('1500.00'), description='Tuition Fee - Term 1', due_date=today + timedelta(days=30), status='paid')
        Fee.objects.create(student=ahmed, amount=Decimal('500.00'), description='Lab Fee', due_date=today + timedelta(days=15), status='unpaid')
        Fee.objects.create(student=omar, amount=Decimal('1500.00'), description='Tuition Fee - Term 1', due_date=today + timedelta(days=30), status='unpaid')
        Fee.objects.create(student=mariam, amount=Decimal('1200.00'), description='Tuition Fee - Term 1', due_date=today + timedelta(days=30), status='paid')
        Fee.objects.create(student=youssef, amount=Decimal('1500.00'), description='Tuition Fee - Term 1', due_date=today - timedelta(days=5), status='unpaid')

        self.stdout.write('Creating warnings...')
        Warning.objects.create(student=omar, issued_by=teacher1, warning_type='behavioral', reason='Disruptive behavior in class.', status='active')
        Warning.objects.create(student=youssef, issued_by=teacher3, warning_type='attendance', reason='Excessive tardiness - late 5 times this month.', status='active')
        Warning.objects.create(student=ahmed, issued_by=teacher1, warning_type='academic', reason='Missing homework assignments.', status='canceled', cancellation_reason='Student completed all missing assignments.')

        self.stdout.write('Creating invitations...')
        ParentInvitation.objects.create(parent=parent1, student=ahmed, date=today + timedelta(days=7), time=time(10, 0), invitation_type='meeting', status='upcoming', notes='Discuss academic progress.')
        ParentInvitation.objects.create(parent=parent2, student=omar, date=today + timedelta(days=3), time=time(14, 30), invitation_type='conference', status='pending', notes='Behavioral discussion.')
        ParentInvitation.objects.create(parent=parent2, student=youssef, date=today - timedelta(days=2), time=time(9, 0), invitation_type='meeting', status='completed', notes='Attendance review - completed.')

        self.stdout.write('Creating homework...')
        Homework.objects.create(school_class=class_5a, assigned_by=teacher1, title='Math Chapter 5 Exercises', content='Complete exercises 1-20 from Chapter 5. Show all working.', due_date=today + timedelta(days=5))
        Homework.objects.create(school_class=class_5a, assigned_by=teacher2, title='Science Project Outline', content='Submit a one-page outline for your science fair project.', due_date=today + timedelta(days=10))
        Homework.objects.create(school_class=class_4a, assigned_by=teacher2, title='English Essay', content='Write a 300-word essay on "My Favorite Season".', due_date=today + timedelta(days=7))
        Homework.objects.create(school_class=class_6a, assigned_by=teacher3, title='History Research', content='Research and summarize the key events of the Industrial Revolution.', due_date=today + timedelta(days=14))

        self.stdout.write('Creating evaluations...')
        Evaluation.objects.create(student=ahmed, teacher=teacher1, subject='Mathematics', grade='A', comment='Excellent problem-solving skills. Shows great understanding of concepts.')
        Evaluation.objects.create(student=ahmed, teacher=teacher2, subject='Science', grade='B+', comment='Good participation. Needs to improve lab report writing.')
        Evaluation.objects.create(student=omar, teacher=teacher1, subject='Mathematics', grade='B', comment='Solid understanding but needs more practice.')
        Evaluation.objects.create(student=mariam, teacher=teacher2, subject='English', grade='A+', comment='Outstanding writing skills and vocabulary.')
        Evaluation.objects.create(student=youssef, teacher=teacher3, subject='History', grade='B-', comment='Good knowledge but needs to participate more in discussions.')

        self.stdout.write('Creating attendance records...')
        for i in range(5):  # Last 5 school days
            d = today - timedelta(days=i+1)
            if d.weekday() < 5:  # weekdays only
                for student in [ahmed, omar, mariam, youssef]:
                    status = 'present'
                    if student == youssef and i < 2:
                        status = 'absent'
                    if student == omar and i == 0:
                        status = 'absent'
                    Attendance.objects.create(student=student, date=d, status=status, marked_by=teacher1)

        self.stdout.write('Creating messages...')
        Message.objects.create(sender=teacher1, recipient=parent1, student=ahmed, subject='Math Progress Update', content='Ahmed is doing very well in mathematics. He scored top marks in the recent test.', is_read=True)
        Message.objects.create(sender=teacher2, recipient=parent1, student=mariam, subject='Science Fair Reminder', content='Please ensure Mariam brings her science project materials next Monday.', is_read=False)
        Message.objects.create(sender=teacher1, recipient=parent2, student=omar, subject='Behavior Concern', content='I wanted to discuss Omar\'s recent behavior in class. Please schedule a meeting.', is_read=False)
        Message.objects.create(sender=teacher3, recipient=parent2, student=youssef, subject='Attendance Notice', content='Youssef has been absent frequently. Please ensure regular attendance.', is_read=True)

        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Teacher: mr_ahmed / teacher123')
        self.stdout.write('  Teacher: ms_sara / teacher123')
        self.stdout.write('  Teacher: mr_mohamed / teacher123')
        self.stdout.write('  Parent:  ahmed_parent / parent123')
        self.stdout.write('  Parent:  omar_parent / parent123')
