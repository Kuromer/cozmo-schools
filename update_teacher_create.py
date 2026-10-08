import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    views_py = f.read()

teacher_create_old = '''@teacher_required
def teacher_message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, teacher=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('teacher_portal:message_list')
    else:
        form = MessageForm(teacher=request.user)
    return render(request, 'teacher_portal/message_form.html', {'form': form})'''

teacher_create_new = '''@teacher_required
def teacher_message_create(request):
    reply_to_id = request.GET.get('reply_to')
    initial = {}
    if reply_to_id:
        try:
            from .models import Message
            original = Message.objects.get(pk=reply_to_id)
            initial['recipient'] = original.sender
            initial['student'] = original.student
            initial['subject'] = f"Re: {original.subject}"
        except Exception:
            pass

    if request.method == 'POST':
        form = MessageForm(request.POST, teacher=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            from django.contrib import messages
            messages.success(request, 'Message sent successfully.')
            return redirect(f"{reverse('teacher_portal:message_list')}?tab=sent")
    else:
        form = MessageForm(initial=initial, teacher=request.user)
    return render(request, 'teacher_portal/message_form.html', {'form': form})'''

views_py = views_py.replace(teacher_create_old, teacher_create_new)

with open('school/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)
