import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''def attendance_view(request):
    class_id = request.GET.get('class_id')
    date_str = request.GET.get('date')
    if not date_str:
        date_str = date.today().isoformat()
    selected_date = date.fromisoformat(date_str)
    
    classes = request.user.assigned_classes.all()
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
        'classes': classes,
        'selected_class': selected_class,
        'selected_date': date_str,
        'students': students,
    }
    return render(request, 'teacher_portal/attendance.html', context)'''

new_func = '''def attendance_view(request):
    tab = request.GET.get('tab', 'take')
    classes = request.user.assigned_classes.all()
    
    if tab == 'history':
        from collections import defaultdict
        # Get all records marked by this teacher
        records = Attendance.objects.filter(marked_by=request.user).select_related('student')
        
        # Pre-fetch students and their classes to avoid N+1
        student_class_map = defaultdict(list)
        from school.models import Student
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
            from datetime import date
            date_str = date.today().isoformat()
        
        from datetime import date
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
            'selected_date': date_str,
            'students': students,
        }
        return render(request, 'teacher_portal/attendance.html', context)'''

if 'def attendance_view(request):' in content and 'history_data =' not in content:
    content = content.replace(old_func, new_func)
    with open('school/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated attendance_view")
else:
    print("attendance_view not found or already updated")
