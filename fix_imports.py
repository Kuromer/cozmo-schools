import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific lines inside attendance_view
content = content.replace("from school.models import Student\n", "")
content = content.replace("from datetime import date\n", "")
content = content.replace("from django.shortcuts import get_object_or_404\n", "")
content = content.replace("from school.models import SchoolClass, Attendance\n", "")

with open('school/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed local imports from attendance_view")
