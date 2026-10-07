from django.contrib import admin
from .models import Student, SchoolClass, Fee, Warning, ParentInvitation, Homework, Evaluation, Attendance, Message

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'parent', 'grade_level', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'grade_level')
    list_filter = ('grade_level', 'enrollment_date')

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'created_at')
    search_fields = ('name', 'grade_level')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'description', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('student__first_name', 'student__last_name', 'description')

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ('student', 'warning_type', 'status', 'issued_by', 'created_at')
    list_filter = ('status', 'warning_type')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(ParentInvitation)
class ParentInvitationAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'invitation_type', 'status', 'date', 'time')
    list_filter = ('status', 'invitation_type', 'date')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'school_class', 'assigned_by', 'due_date', 'created_at')
    list_filter = ('due_date', 'school_class')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'teacher', 'created_at')
    list_filter = ('subject', 'grade')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'student', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
