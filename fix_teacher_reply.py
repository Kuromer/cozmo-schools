import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''def teacher_message_create(request):
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
    return render(request, 'teacher_portal/message_form.html', {'form': form, 'is_reply': bool(reply_to_id)})'''

new_func = '''def teacher_message_create(request):
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
    return render(request, 'teacher_portal/message_form.html', {'form': form, 'is_reply': bool(reply_to_id)})'''

content = content.replace(old_func, new_func)

with open('school/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
