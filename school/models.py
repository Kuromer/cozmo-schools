from django.db import models
from django.conf import settings

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='children', limit_choices_to={'role': 'parent'})
    grade_level = models.CharField(max_length=50, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['first_name', 'last_name']

class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_classes', limit_choices_to={'role': 'teacher'}, blank=True)
    students = models.ManyToManyField(Student, related_name='classes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'School Classes'
        ordering = ['name']

    def __str__(self):
        return self.name

class Fee(models.Model):
    STATUS_CHOICES = (('paid', 'Paid'), ('unpaid', 'Unpaid'))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.description} ({self.status})"

    class Meta:
        ordering = ['-created_at']

class Warning(models.Model):
    STATUS_CHOICES = (('active', 'Active'), ('canceled', 'Canceled'))
    WARNING_TYPES = (('behavioral', 'Behavioral'), ('academic', 'Academic'), ('attendance', 'Attendance'), ('other', 'Other'))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='warnings')
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    warning_type = models.CharField(max_length=20, choices=WARNING_TYPES)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Warning: {self.student} - {self.get_warning_type_display()}"

    class Meta:
        ordering = ['-created_at']

class ParentInvitation(models.Model):
    STATUS_CHOICES = (('upcoming', 'Upcoming'), ('pending', 'Pending'), ('completed', 'Completed'), ('rescheduled', 'Rescheduled'))
    INVITATION_TYPES = (('meeting', 'Parent Meeting'), ('conference', 'Conference'), ('event', 'School Event'), ('other', 'Other'))
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations', limit_choices_to={'role': 'parent'})
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invitations')
    date = models.DateField()
    time = models.TimeField()
    invitation_type = models.CharField(max_length=20, choices=INVITATION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation: {self.parent} - {self.get_invitation_type_display()}"

    class Meta:
        ordering = ['-date', '-time']

class Homework(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='homework_assignments')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_homework')
    title = models.CharField(max_length=255)
    content = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.school_class}"

    class Meta:
        ordering = ['-created_at']

class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='evaluations')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='evaluations_given')
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"

    class Meta:
        ordering = ['-created_at']

class Attendance(models.Model):
    STATUS_CHOICES = (('present', 'Present'), ('absent', 'Absent'))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date}: {self.status}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.subject}"

    class Meta:
        ordering = ['-created_at']
