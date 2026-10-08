import re

with open('templates/parent_portal/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

def add_link(title_text, url_name):
    global html
    # Find the h3 that contains the title text
    pattern = r'(<h3[^>]*>.*?'+title_text+r'\s*</h3>)'
    replacement = r'<div class="flex justify-between items-center mb-4">\n                \1\n                <a href="{% url \'' + url_name + r'\' %}?child_id={{ selected_child.id }}" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">View all &rarr;</a>\n            </div>'
    
    # We also want to remove mb-4 from the h3 itself if it exists, so we don't have double margins
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

add_link('Attendance Overview', 'parent_portal:attendance')
add_link('Financial Status', 'parent_portal:fees')
add_link('Active Warnings', 'parent_portal:warnings')
add_link('Upcoming Invitations', 'parent_portal:invitations')
add_link('Recent Homework', 'parent_portal:homework')
add_link('Latest Evaluations', 'parent_portal:evaluations')
add_link('Recent Messages', 'parent_portal:messages')

# Now fix the mb-4 in the h3s that we wrapped
html = re.sub(r'(<div class="flex justify-between items-center mb-4">\s*<h3 class="[^"]*?)\s*mb-4\s*([^"]*">)', r'\1 \2', html)

with open('templates/parent_portal/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
