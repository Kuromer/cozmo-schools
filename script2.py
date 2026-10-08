import re

with open('templates/parent_portal/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

def inject_view_all(section_name, url_name):
    global html
    # The regex matches the h3 tag, the svg (if any), the text, and the closing h3 tag
    pattern = r'(<h3 class="text-lg font-semibold text-gray-900 mb-4(?: flex items-center gap-2)?">)(\s*(?:<svg.*?</svg>\s*)?' + section_name + r'\s*</h3>)'
    
    # We replace the h3's mb-4 class so the outer div has the margin instead
    def repl(m):
        h3_start = m.group(1).replace(' mb-4', '')
        inner_content = m.group(2)
        url = "{% url 'parent_portal:" + url_name + "' %}"
        link = f'<a href="{url}?child_id={{{{ selected_child.id }}}}" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">View all &rarr;</a>'
        return f'<div class="flex justify-between items-center mb-4">\n                {h3_start}{inner_content}\n                {link}\n            </div>'
        
    html = re.sub(pattern, repl, html, flags=re.DOTALL)

inject_view_all('Attendance Overview', 'attendance')
inject_view_all('Financial Overview', 'fees')
inject_view_all('Active Warnings', 'warnings')
inject_view_all('Upcoming Invitations', 'invitations')
inject_view_all('Recent Homework', 'homework')
inject_view_all('Evaluations', 'evaluations')
inject_view_all('Recent Messages', 'messages')

with open('templates/parent_portal/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
