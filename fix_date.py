with open('school/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = "from datetime import date\n" + content

with open('school/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
