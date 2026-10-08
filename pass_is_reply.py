import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update parent_message_create
# from:
#     return render(request, 'parent_portal/message_form.html', {
#         'form': form,
#         'children': children,
#         'selected_child': selected_child
#     })
# to include 'is_reply': bool(reply_to_id)
old_pmc_render = '''    return render(request, 'parent_portal/message_form.html', {
        'form': form,
        'children': children,
        'selected_child': selected_child
    })'''
new_pmc_render = '''    return render(request, 'parent_portal/message_form.html', {
        'form': form,
        'children': children,
        'selected_child': selected_child,
        'is_reply': bool(reply_to_id)
    })'''
content = content.replace(old_pmc_render, new_pmc_render)

# Update teacher_message_create
old_tmc_render = '''    return render(request, 'teacher_portal/message_form.html', {'form': form})'''
new_tmc_render = '''    return render(request, 'teacher_portal/message_form.html', {'form': form, 'is_reply': bool(reply_to_id)})'''
content = content.replace(old_tmc_render, new_tmc_render)

with open('school/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
