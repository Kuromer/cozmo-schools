from datetime import date
import io
import csv
import openpyxl

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

from accounts.decorators import admin_required, teacher_required, parent_required
from accounts.models import CustomUser
from .models import (
    Student, SchoolClass, Fee, Warning, ParentInvitation, 
    Homework, Evaluation, Attendance, Message
)
from .forms import (
    StudentForm, FeeForm, WarningForm, CancelWarningForm, 
    ParentInvitationForm, InvitationUpdateForm, HomeworkForm, 
    EvaluationForm, MessageForm
)

# ================= ADMIN VIEWS =================

@admin_required
def admin_dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': CustomUser.objects.filter(role='teacher').count(),
        'unpaid_fees_count': Fee.objects.filter(status='unpaid').count(),
        'active_warnings_count': Warning.objects.filter(status='active').count(),
        'pending_invitations_count': ParentInvitation.objects.filter(status='pending').count(),
        'recent_students': Student.objects.order_by('-created_at')[:5],
        'recent_warnings': Warning.objects.filter(status='active').order_by('-created_at')[:5],
    }
    return render(request, 'admin_portal/dashboard.html', context)

@admin_required
def student_list(request):
    students = Student.objects.select_related('parent').all()
    return render(request, 'admin_portal/student_list.html', {'students': students})

@admin_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('admin_portal:student_list')
    else:
        form = StudentForm()
    return render(request, 'admin_portal/student_form.html', {'form': form, 'title': 'Add New Student'})

@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('admin_portal:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin_portal/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})

@admin_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('admin_portal:student_list')
    return redirect('admin_portal:student_list')

@admin_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {
        'student': student,
        'fees': student.fees.all(),
        'warnings': student.warnings.all(),
        'invitations': student.invitations.all(),
        'homework_list': Homework.objects.filter(school_class__students=student),
        'evaluations': student.evaluations.all(),
        'attendance_records': student.attendance_records.all(),
        'school_messages': student.messages.all(),
    }
    return render(request, 'admin_portal/student_detail.html', context)

@admin_required
def finance_list(request):
    status_filter = request.GET.get('status')
    if status_filter == 'unpaid':
        fees = Fee.objects.filter(status='unpaid').select_related('student')
    else:
        fees = Fee.objects.all().select_related('student')
    return render(request, 'admin_portal/finance.html', {'fees': fees, 'current_filter': status_filter})

@admin_required
def fee_create(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee added successfully.')
            return redirect('admin_portal:finance_list')
    else:
        form = FeeForm()
    return render(request, 'admin_portal/fee_form.html', {'form': form, 'title': 'Create New Fee Record', 'btn_text': 'Add Fee'})

@admin_required
def fee_edit(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, 'Fee updated successfully.')
            return redirect('admin_portal:finance_list')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'admin_portal/fee_form.html', {'form': form, 'title': 'Edit Fee Record', 'btn_text': 'Update Fee'})


@admin_required
def fee_toggle(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        fee.status = 'paid' if fee.status == 'unpaid' else 'unpaid'
        fee.save()
        messages.success(request, 'Fee status updated.')
    return redirect('admin_portal:finance_list')

@admin_required
def warning_list(request):
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        warnings = Warning.objects.filter(status=status_filter)
    else:
        warnings = Warning.objects.all()
    return render(request, 'admin_portal/warnings.html', {'warnings': warnings, 'current_filter': status_filter})

@admin_required
def warning_create(request):
    if request.method == 'POST':
        form = WarningForm(request.POST)
        if form.is_valid():
            warning = form.save(commit=False)
            warning.issued_by = request.user
            warning.save()
            messages.success(request, 'Warning issued successfully.')
            return redirect('admin_portal:warning_list')
    else:
        form = WarningForm()
    return render(request, 'admin_portal/warning_form.html', {'form': form})

@admin_required
def warning_cancel(request, pk):
    warning = get_object_or_404(Warning, pk=pk)
    if request.method == 'POST':
        form = CancelWarningForm(request.POST)
        if form.is_valid():
            warning.status = 'canceled'
            warning.cancellation_reason = form.cleaned_data['cancellation_reason']
            warning.save()
            messages.success(request, 'Warning canceled successfully.')
            return redirect('admin_portal:warning_list')
    else:
        form = CancelWarningForm()
    return render(request, 'admin_portal/cancel_warning.html', {'form': form, 'warning': warning})

@admin_required
def invitation_list(request):
    invitations = ParentInvitation.objects.all()
    return render(request, 'admin_portal/invitations.html', {'invitations': invitations})

@admin_required
def invitation_create(request):
    if request.method == 'POST':
        form = ParentInvitationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invitation created successfully.')
            return redirect('admin_portal:invitation_list')
    else:
        form = ParentInvitationForm()
    return render(request, 'admin_portal/invitation_form.html', {'form': form})

@admin_required
def invitation_update(request, pk):
    invitation = get_object_or_404(ParentInvitation, pk=pk)
    if request.method == 'POST':
        form = InvitationUpdateForm(request.POST, instance=invitation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invitation updated successfully.')
            return redirect('admin_portal:invitation_list')
    else:
        form = InvitationUpdateForm(instance=invitation)
    return render(request, 'admin_portal/invitation_update.html', {'form': form, 'invitation': invitation})

@admin_required
def reports(request):
    report_type = request.GET.get('type', 'class_list')
    class_id = request.GET.get('class_id')
    classes = SchoolClass.objects.all()

    data = []
    if report_type == 'class_list':
        if class_id:
            data = Student.objects.filter(classes__id=class_id).select_related('parent')
        else:
            data = Student.objects.all().select_related('parent')
    elif report_type == 'unpaid_students':
        # Return Fee objects so template can access row.student, row.description, row.amount
        data = Fee.objects.filter(status='unpaid').select_related('student', 'student__parent')
    elif report_type == 'warnings':
        # Return Warning objects so template can access row.student, row.get_warning_type_display
        data = Warning.objects.filter(status='active').select_related('student')
    elif report_type == 'full':
        data = Student.objects.all().select_related('parent')

    context = {
        'report_type': report_type,
        'data': data,
        'classes': classes,
    }
    return render(request, 'admin_portal/reports.html', context)

@admin_required
def export_report(request):
    report_type = request.GET.get('type', 'class_list')
    format_type = request.GET.get('format', 'csv')
    class_id = request.GET.get('class_id')

    # Build headers and rows based on report type
    if report_type == 'unpaid_students':
        queryset = Fee.objects.filter(status='unpaid').select_related('student', 'student__parent')
        headers = ['Student Name', 'Grade', 'Fee Description', 'Amount', 'Due Date']
        def get_row(obj):
            return [obj.student.full_name, obj.student.grade_level, obj.description, str(obj.amount), str(obj.due_date)]
    elif report_type == 'warnings':
        queryset = Warning.objects.filter(status='active').select_related('student')
        headers = ['Student Name', 'Grade', 'Warning Type', 'Date Issued']
        def get_row(obj):
            return [obj.student.full_name, obj.student.grade_level, obj.get_warning_type_display(), str(obj.created_at.date())]
    else:
        if report_type == 'class_list' and class_id:
            queryset = Student.objects.filter(classes__id=class_id).select_related('parent')
        else:
            queryset = Student.objects.all().select_related('parent')
        headers = ['ID', 'First Name', 'Last Name', 'Grade Level', 'Parent']
        def get_row(obj):
            return [obj.id, obj.first_name, obj.last_name, obj.grade_level, str(obj.parent) if obj.parent else '']

    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        for obj in queryset:
            writer.writerow(get_row(obj))
        return response

    elif format_type == 'excel':
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Report'
        sheet.append(headers)
        for obj in queryset:
            sheet.append(get_row(obj))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.xlsx"'
        workbook.save(response)
        return response

    return redirect('admin_portal:reports')


# ================= TEACHER VIEWS =================

@teacher_required
def teacher_dashboard(request):
    from django.db.models import Count
    classes = request.user.assigned_classes.all().annotate(student_count=Count('students'))
    
    context = {'classes': classes}
    return render(request, 'teacher_portal/dashboard.html', context)

@teacher_required
def teacher_class_detail(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk, teachers=request.user)
    students = school_class.students.all()
    context = {'school_class': school_class, 'students': students}
    return render(request, 'teacher_portal/class_detail.html', context)

@teacher_required
def homework_list(request):
    homework_list = Homework.objects.filter(assigned_by=request.user)
    context = {'homework_list': homework_list}
    return render(request, 'teacher_portal/homework_list.html', context)

@teacher_required
def homework_create(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST, teacher=request.user)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.assigned_by = request.user
            homework.subject = request.user.subject
            homework.save()
            messages.success(request, 'Homework assigned successfully.')
            return redirect('teacher_portal:homework_list')
    else:
        form = HomeworkForm(teacher=request.user)
    return render(request, 'teacher_portal/homework_form.html', {'form': form})

@teacher_required
def homework_edit(request, pk):
    homework = get_object_or_404(Homework, pk=pk, assigned_by=request.user)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=homework, teacher=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Homework updated successfully.')
            return redirect('teacher_portal:homework_list')
    else:
        form = HomeworkForm(instance=homework, teacher=request.user)
    return render(request, 'teacher_portal/homework_form.html', {'form': form, 'title': 'Edit Homework'})

@teacher_required
def homework_delete(request, pk):
    homework = get_object_or_404(Homework, pk=pk, assigned_by=request.user)
    if request.method == 'POST':
        homework.delete()
        messages.success(request, 'Homework deleted successfully.')
    return redirect('teacher_portal:homework_list')
@teacher_required
def teacher_message_list(request):
    tab = request.GET.get('tab', 'inbox')
    if tab == 'sent':
        messages_list = Message.objects.filter(sender=request.user).order_by('-created_at')
    else:
        messages_list = Message.objects.filter(recipient=request.user).order_by('-created_at')
        
    return render(request, 'teacher_portal/messages.html', {
        'school_messages': messages_list,
        'tab': tab
    })

@teacher_required
def teacher_message_create(request):
    reply_to_id = request.GET.get('reply_to')
    initial = {}
    if reply_to_id:
        try:
            original = Message.objects.get(pk=reply_to_id)
            initial['recipient'] = original.sender
            initial['student'] = original.student
            initial['subject'] = f"Re: {original.subject}"
        except Message.DoesNotExist:
            pass

    if request.method == 'POST':
        form = MessageForm(request.POST, teacher=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('teacher_portal:message_list')
    else:
        form = MessageForm(initial=initial, teacher=request.user)
    return render(request, 'teacher_portal/message_form.html', {'form': form, 'is_reply': bool(reply_to_id)})

@teacher_required
def evaluation_list(request):
    evaluations = Evaluation.objects.filter(teacher=request.user)
    return render(request, 'teacher_portal/evaluations.html', {'evaluations': evaluations})

@teacher_required
def evaluation_create(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST, teacher=request.user)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.teacher = request.user
            evaluation.subject = request.user.subject
            evaluation.save()
            messages.success(request, 'Evaluation added successfully.')
            return redirect('teacher_portal:evaluation_list')
    else:
        form = EvaluationForm(teacher=request.user)
    return render(request, 'teacher_portal/evaluation_form.html', {'form': form})

@teacher_required
def attendance_view(request):
    tab = request.GET.get('tab', 'take')
    classes = request.user.assigned_classes.all()
    
    if tab == 'history':
        from collections import defaultdict
        records = Attendance.objects.filter(marked_by=request.user).select_related('student')
        
        student_class_map = defaultdict(list)
        for s in Student.objects.filter(classes__in=classes).prefetch_related('classes'):
            student_class_map[s.id] = [c for c in s.classes.all() if c in classes]
            
        history_data = {}
        for record in records:
            shared_classes = student_class_map.get(record.student_id, [])
            for c in shared_classes:
                key = (record.date, c.id)
                if key not in history_data:
                    history_data[key] = {'date': record.date, 'class': c, 'present': 0, 'absent': 0, 'total': 0}
                
                history_data[key]['total'] += 1
                if record.status == 'present':
                    history_data[key]['present'] += 1
                else:
                    history_data[key]['absent'] += 1
                    
        history_list = sorted(history_data.values(), key=lambda x: x['date'], reverse=True)
        return render(request, 'teacher_portal/attendance.html', {'tab': tab, 'history_list': history_list})
        
    else:
        class_id = request.GET.get('class_id')
        date_str = request.GET.get('date')
        if not date_str:
            date_str = date.today().isoformat()
        
        selected_date = date.fromisoformat(date_str)
        
        selected_class = None
        students = []
        attendance_records = {}
        
        if class_id:
            selected_class = get_object_or_404(SchoolClass, pk=class_id, teachers=request.user)
            students = list(selected_class.students.all())
            records = Attendance.objects.filter(student__in=students, date=selected_date, subject=request.user.subject)
            attendance_records = {record.student_id: record.status for record in records}
            for student in students:
                student.current_status = attendance_records.get(student.id, '')
            
        context = {
            'tab': tab,
            'classes': classes,
            'selected_class': selected_class,
            'selected_date': selected_date.isoformat(),
            'students': students,
            'attendance_records': attendance_records,
        }
        return render(request, 'teacher_portal/attendance.html', context)

@teacher_required
def attendance_mark(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        date_str = request.POST.get('date')
        if not date_str:
            date_str = date.today().isoformat()
        selected_date = date.fromisoformat(date_str)
        selected_class = get_object_or_404(SchoolClass, pk=class_id, teachers=request.user)
        students = selected_class.students.all()
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['present', 'absent']:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    subject=request.user.subject,
                    defaults={'status': status, 'marked_by': request.user}
                )
        messages.success(request, 'Attendance marked successfully.')
        return redirect(f"/teacher/attendance/?class_id={class_id}&date={date_str}")
    return redirect('teacher_portal:attendance_view')


# ================= PARENT VIEWS =================

@parent_required
def parent_dashboard(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = None
    
    if children.exists():
        if child_id:
            selected_child = get_object_or_404(Student, pk=child_id, parent=request.user)
        else:
            selected_child = children.first()
            
    context = {
        'children': children,
        'selected_child': selected_child,
    }
    
    if selected_child:
        context.update({
            'fees': selected_child.fees.all(),
            'warnings': selected_child.warnings.all(),
            'invitations': selected_child.invitations.all(),
            'homework_list': Homework.objects.filter(school_class__students=selected_child),
            'evaluations': selected_child.evaluations.all(),
            'school_messages': Message.objects.filter(recipient=request.user, student=selected_child),
            'attendance_records': selected_child.attendance_records.all(),
        })
        
    return render(request, 'parent_portal/dashboard.html', context)
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

@admin_required
def user_list(request):
    role_filter = request.GET.get('role', 'all')
    if role_filter != 'all':
        users = CustomUser.objects.filter(role=role_filter).order_by('role', 'username')
    else:
        users = CustomUser.objects.all().order_by('role', 'username')
    return render(request, 'admin_portal/user_list.html', {'users': users, 'current_filter': role_filter})

@admin_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account created successfully.')
            return redirect('admin_portal:user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_portal/user_form.html', {'form': form, 'title': 'Create User Account'})

@admin_required
def user_edit(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account updated successfully.')
            return redirect('admin_portal:user_list')
    else:
        form = CustomUserChangeForm(instance=user_obj)
    return render(request, 'admin_portal/user_form.html', {'form': form, 'title': 'Edit User Account'})

@admin_required
def user_delete(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if request.user == user_obj:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_portal:user_list')
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, 'User account deleted successfully.')
    return redirect('admin_portal:user_list')

from .forms import SchoolClassForm

@admin_required
def class_list(request):
    classes = SchoolClass.objects.prefetch_related('teachers', 'students').all()
    return render(request, 'admin_portal/class_list.html', {'classes': classes})

@admin_required
def class_create(request):
    if request.method == 'POST':
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully.')
            return redirect('admin_portal:class_list')
    else:
        form = SchoolClassForm()
    return render(request, 'admin_portal/class_form.html', {'form': form, 'title': 'Create New Class'})

@admin_required
def class_edit(request, pk):
    class_obj = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        form = SchoolClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('admin_portal:class_list')
    else:
        form = SchoolClassForm(instance=class_obj)
    return render(request, 'admin_portal/class_form.html', {'form': form, 'title': 'Edit Class'})

@admin_required
def class_delete(request, pk):
    class_obj = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Class deleted successfully.')
    return redirect('admin_portal:class_list')
@parent_required
def parent_fees(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    fees = selected_child.fees.all() if selected_child else []
    return render(request, 'parent_portal/fees.html', {'children': children, 'selected_child': selected_child, 'fees': fees})

@parent_required
def parent_warnings(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    warnings = selected_child.warnings.all() if selected_child else []
    return render(request, 'parent_portal/warnings.html', {'children': children, 'selected_child': selected_child, 'warnings': warnings})

@parent_required
def parent_invitations(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    invitations = selected_child.invitations.all() if selected_child else []
    return render(request, 'parent_portal/invitations.html', {'children': children, 'selected_child': selected_child, 'invitations': invitations})

@parent_required
def parent_homework(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    homework_list = Homework.objects.filter(school_class__students=selected_child) if selected_child else []
    return render(request, 'parent_portal/homework.html', {'children': children, 'selected_child': selected_child, 'homework_list': homework_list})

@parent_required
def parent_evaluations(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    evaluations = selected_child.evaluations.all() if selected_child else []
    return render(request, 'parent_portal/evaluations.html', {'children': children, 'selected_child': selected_child, 'evaluations': evaluations})

@parent_required
def parent_messages(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    
    tab = request.GET.get('tab', 'inbox')
    if selected_child:
        if tab == 'sent':
            school_messages = Message.objects.filter(sender=request.user, student=selected_child).order_by('-created_at')
        else:
            school_messages = Message.objects.filter(recipient=request.user, student=selected_child).order_by('-created_at')
    else:
        school_messages = []
        
    return render(request, 'parent_portal/messages.html', {
        'children': children, 
        'selected_child': selected_child, 
        'school_messages': school_messages,
        'tab': tab
    })

@parent_required
def parent_attendance(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    attendance_records = selected_child.attendance_records.all() if selected_child else []
    return render(request, 'parent_portal/attendance.html', {'children': children, 'selected_child': selected_child, 'attendance_records': attendance_records})

@parent_required
def parent_message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.recipient != request.user and msg.sender != request.user:
        from django.http import Http404
        raise Http404("Not authorized")
        
    if msg.recipient == request.user and not msg.is_read:
        msg.is_read = True
        msg.save()
        
    children = request.user.children.all()
    selected_child = msg.student if msg.student in children else children.first()
    return render(request, 'parent_portal/message_detail.html', {'msg': msg, 'children': children, 'selected_child': selected_child})

@parent_required
def parent_message_create(request):
    children = request.user.children.all()
    child_id = request.GET.get('child_id')
    selected_child = get_object_or_404(Student, pk=child_id, parent=request.user) if child_id else children.first()
    
    reply_to_id = request.GET.get('reply_to')
    initial = {}
    if reply_to_id:
        try:
            original = Message.objects.get(pk=reply_to_id)
            initial['recipient'] = original.sender
            initial['subject'] = f"Re: {original.subject}"
        except Message.DoesNotExist:
            pass

    if request.method == 'POST':
        from .forms import ParentMessageForm
        form = ParentMessageForm(request.POST, parent=request.user, child=selected_child)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.student = selected_child
            msg.save()
            from django.contrib import messages
            messages.success(request, 'Message sent successfully.')
            return redirect(f"{reverse('parent_portal:messages')}?child_id={selected_child.id}&tab=sent")
    else:
        from .forms import ParentMessageForm
        form = ParentMessageForm(initial=initial, parent=request.user, child=selected_child)

    return render(request, 'parent_portal/message_form.html', {
        'form': form,
        'children': children,
        'selected_child': selected_child,
        'is_reply': bool(reply_to_id)
    })

@teacher_required
def teacher_message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.recipient != request.user and msg.sender != request.user:
        from django.http import Http404
        raise Http404("Not authorized")
        
    if msg.recipient == request.user and not msg.is_read:
        msg.is_read = True
        msg.save()
        
    return render(request, 'teacher_portal/message_detail.html', {'msg': msg})

@parent_required
def parent_warning_detail(request, pk):
    warning = get_object_or_404(Warning, pk=pk)
    # Ensure the parent is authorized to view this warning
    children = request.user.children.all()
    if warning.student not in children:
        from django.http import Http404
        raise Http404("Not authorized")
        
    selected_child = warning.student
    return render(request, 'parent_portal/warning_detail.html', {
        'warning': warning, 
        'children': children, 
        'selected_child': selected_child
    })
