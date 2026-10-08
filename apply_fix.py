import os

def replace_in_file(filepath, old_text, new_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Text not found in {filepath}")

# Update finance.html
old_finance = '''                    <td class="px-6 py-4 whitespace-nowrap text-right">
                        <form action="{% url 'admin_portal:fee_toggle' fee.id %}" method="post">'''
new_finance = '''                    <td class="px-6 py-4 whitespace-nowrap text-right flex justify-end items-center gap-3">
                        <a href="{% url 'admin_portal:fee_edit' fee.id %}" class="text-sm font-medium text-amber-600 hover:text-amber-800">Edit</a>
                        <form action="{% url 'admin_portal:fee_toggle' fee.id %}" method="post" class="inline">'''
replace_in_file('templates/admin_portal/finance.html', old_finance, new_finance)

# Update student_detail.html
old_student = '''                    <td class="px-6 py-4 text-right">
                        <form action="{% url 'admin_portal:fee_toggle' fee.id %}" method="post">'''
new_student = '''                    <td class="px-6 py-4 text-right flex justify-end items-center gap-3">
                        <a href="{% url 'admin_portal:fee_edit' fee.id %}" class="text-sm font-medium text-amber-600 hover:text-amber-800">Edit</a>
                        <form action="{% url 'admin_portal:fee_toggle' fee.id %}" method="post" class="inline">'''
replace_in_file('templates/admin_portal/student_detail.html', old_student, new_student)

