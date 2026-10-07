import io
import csv
from datetime import date
import openpyxl

from django.shortcuts import render, redirect, get_object_or_404
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
        'messages': student.messages.all(),
    }
    return render(request, 'admin_portal/student_detail.html', context)

@admin_required
def finance_list(request):
    status_filter = request.GET.get('status')
    if status_filter == 'unpaid':
        fees = Fee.objects.filter(status='unpaid')
    else:
        fees = Fee.objects.all()
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
    return render(request, 'admin_portal/fee_form.html', {'form': form})

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
    if status_filter:
        warnings = Warning.objects.filter(status=status_filter)
    else:
        warnings = Warning.objects.all()
    return render(request, 'admin_portal/warnings.html', {'warnings': warnings})

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
            data = Student.objects.filter(classes__id=class_id)
        else:
            data = Student.objects.all()
    elif report_type == 'unpaid':
        data = Student.objects.filter(fees__status='unpaid').distinct()
    elif report_type == 'warnings':
        data = Student.objects.filter(warnings__status='active').distinct()
    elif report_type == 'full':
        data = Student.objects.all()
        
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
    
    if report_type == 'unpaid':
        data = Student.objects.filter(fees__status='unpaid').distinct()
    elif report_type == 'warnings':
        data = Student.objects.filter(warnings__status='active').distinct()
    else:
        data = Student.objects.all()
        
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'First Name', 'Last Name', 'Grade Level', 'Parent'])
        for student in data:
            writer.writerow([student.id, student.first_name, student.last_name, student.grade_level, student.parent])
        return response
        
    elif format_type == 'excel':
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Report'
        sheet.append(['ID', 'First Name', 'Last Name', 'Grade Level', 'Parent'])
        for student in data:
            sheet.append([student.id, student.first_name, student.last_name, student.grade_level, str(student.parent)])
            
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
            homework.save()
            messages.success(request, 'Homework assigned successfully.')
            return redirect('teacher_portal:homework_list')
    else:
        form = HomeworkForm(teacher=request.user)
    return render(request, 'teacher_portal/homework_form.html', {'form': form})

@teacher_required
def teacher_message_list(request):
    messages_list = Message.objects.filter(sender=request.user)
    return render(request, 'teacher_portal/messages.html', {'messages': messages_list})

@teacher_required
def teacher_message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, teacher=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('teacher_portal:message_list')
    else:
        form = MessageForm(teacher=request.user)
    return render(request, 'teacher_portal/message_form.html', {'form': form})

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
            evaluation.save()
            messages.success(request, 'Evaluation added successfully.')
            return redirect('teacher_portal:evaluation_list')
    else:
        form = EvaluationForm(teacher=request.user)
    return render(request, 'teacher_portal/evaluation_form.html', {'form': form})

@teacher_required
def attendance_view(request):
    class_id = request.GET.get('class_id')
    date_str = request.GET.get('date', date.today().isoformat())
    selected_date = date.fromisoformat(date_str)
    
    classes = request.user.assigned_classes.all()
    selected_class = None
    students = []
    attendance_records = {}
    
    if class_id:
        selected_class = get_object_or_404(SchoolClass, pk=class_id, teachers=request.user)
        students = selected_class.students.all()
        records = Attendance.objects.filter(student__in=students, date=selected_date)
        attendance_records = {record.student_id: record.status for record in records}
        
    context = {
        'classes': classes,
        'selected_class': selected_class,
        'selected_date': selected_date,
        'students': students,
        'attendance_records': attendance_records,
    }
    return render(request, 'teacher_portal/attendance.html', context)

@teacher_required
def attendance_mark(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        date_str = request.POST.get('date')
        selected_date = date.fromisoformat(date_str)
        selected_class = get_object_or_404(SchoolClass, pk=class_id, teachers=request.user)
        students = selected_class.students.all()
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['present', 'absent']:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
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
            'messages': Message.objects.filter(recipient=request.user, student=selected_child),
            'attendance_records': selected_child.attendance_records.all(),
        })
        
    return render(request, 'parent_portal/dashboard.html', context)
