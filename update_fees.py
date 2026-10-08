import re

# 1. Update views.py
with open('school/views.py', 'r', encoding='utf-8') as f:
    views_py = f.read()

fee_edit_view = '''
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
'''

if 'def fee_edit' not in views_py:
    # insert after fee_create
    pattern = r'(def fee_create\(request\):.*?return render\(request, \'admin_portal/fee_form\.html\', \{.*?\}\))'
    # we also need to update fee_create to pass 'title'
    def repl(m):
        old = m.group(1)
        old = old.replace("{'form': form}", "{'form': form, 'title': 'Create New Fee Record', 'btn_text': 'Add Fee'}")
        return old + '\n' + fee_edit_view
    
    views_py = re.sub(pattern, repl, views_py, flags=re.DOTALL)
    
    with open('school/views.py', 'w', encoding='utf-8') as f:
        f.write(views_py)
    print("Updated views.py")
