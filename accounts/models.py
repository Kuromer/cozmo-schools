from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    SUBJECT_CHOICES = (
        ('arabic', 'Arabic'),
        ('english', 'English'),
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('social_studies', 'Social Studies'),
        ('computer', 'Computer Science'),
        ('art', 'Art'),
        ('pe', 'Physical Education'),
        ('religion', 'Religion'),
        ('second_language', 'Second Language'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, blank=True, help_text="For Teachers only")

    def is_admin_user(self):
        return self.role == 'admin'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_parent(self):
        return self.role == 'parent'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
