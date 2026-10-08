import re

with open('templates/parent_portal/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

sections = [
    ('Attendance Overview', 'attendance'),
    ('Financial Overview', 'fees'),
    ('Active Warnings', 'warnings'),
    ('Recent Homework', 'homework'),
    ('Evaluations', 'evaluations'),
    ('Recent Messages', 'messages')
]

for title, url_name in sections:
    # Match EXACTLY the h3 block for this section.
    # Non-greedy .*? between <h3 and </h3> that must contain the title.
    pattern = r'(<h3[^>]*>.*?'+title+r'.*?</h3>)'
    
    def repl(m):
        full_h3 = m.group(1)
        # Remove mb-4 from inside the h3 tag
        full_h3 = full_h3.replace(' mb-4', '')
        
        url = f"{{% url 'parent_portal:{url_name}' %}}"
        link = f'<a href="{url}?child_id={{{{ selected_child.id }}}}" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">View all &rarr;</a>'
        return f'<div class="flex justify-between items-center mb-4">\n                {full_h3}\n                {link}\n            </div>'

    html = re.sub(pattern, repl, html, flags=re.DOTALL)

with open('templates/parent_portal/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
