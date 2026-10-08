import os
import re

files = [
    'attendance.html',
    'evaluations.html',
    'fees.html',
    'homework.html',
    'invitations.html',
    'warnings.html'
]

toggle_html = '''<div class="mb-6 overflow-x-auto pb-2">
    <div class="flex space-x-2">
        {% for child in children %}
        <a href="?child_id={{ child.id }}" 
           class="px-5 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap {% if selected_child.id == child.id %}bg-emerald-600 text-white shadow-md{% else %}bg-white text-gray-600 border border-gray-200 hover:bg-gray-50{% endif %}">
            {{ child.full_name }}
        </a>
        {% endfor %}
    </div>
</div>'''

for f in files:
    path = os.path.join('templates/parent_portal', f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # The current top block is usually:
    # <div class="mb-6 flex justify-between items-center">
    #     <a href=...
    #     <h2...
    # </div>
    pattern = r'<div class="mb-6 flex justify-between items-center">.*?</div>'
    
    # Replace the block with our toggle_html
    new_content = re.sub(pattern, toggle_html, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print(f"Updated {f}")
