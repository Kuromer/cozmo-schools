import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    views_py = f.read()

# 1. Update parent_messages to include received and sent messages
new_parent_messages = '''def parent_messages(request):
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
    })'''
views_py = re.sub(r'def parent_messages\(request\):.*?return render\(.*?parent_portal/messages\.html.*?\}\)', new_parent_messages, views_py, flags=re.DOTALL)

# 2. Add parent_message_detail and parent_message_create
parent_new_views = '''
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
        'selected_child': selected_child
    })
'''

# 3. Update teacher_message_list to include received and sent messages
new_teacher_messages = '''def teacher_message_list(request):
    tab = request.GET.get('tab', 'inbox')
    if tab == 'sent':
        messages_list = Message.objects.filter(sender=request.user).order_by('-created_at')
    else:
        messages_list = Message.objects.filter(recipient=request.user).order_by('-created_at')
        
    return render(request, 'teacher_portal/messages.html', {
        'school_messages': messages_list,
        'tab': tab
    })'''
views_py = re.sub(r'def teacher_message_list\(request\):.*?return render\(.*?teacher_portal/messages\.html.*?\}\)', new_teacher_messages, views_py, flags=re.DOTALL)

# 4. Add teacher_message_detail
teacher_new_views = '''
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
'''

# Check if parent_message_detail is already added to avoid duplication
if 'def parent_message_detail' not in views_py:
    views_py += parent_new_views

if 'def teacher_message_detail' not in views_py:
    views_py += teacher_new_views

# Fix import for reverse
if 'from django.urls import reverse' not in views_py:
    views_py = views_py.replace('from django.shortcuts import render, redirect, get_object_or_404', 'from django.shortcuts import render, redirect, get_object_or_404\nfrom django.urls import reverse')

with open('school/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

print("Updated views.py")
