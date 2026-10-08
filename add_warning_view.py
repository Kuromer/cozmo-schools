import re

with open('school/views.py', 'r', encoding='utf-8') as f:
    views_py = f.read()

warning_view = '''
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
'''

if 'def parent_warning_detail' not in views_py:
    views_py += warning_view
    with open('school/views.py', 'w', encoding='utf-8') as f:
        f.write(views_py)
    print("Added parent_warning_detail view.")
