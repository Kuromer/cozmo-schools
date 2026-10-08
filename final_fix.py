import re

with open('templates/admin_portal/user_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the field div wrapper logic
old_div = '''                    <div class="{% if field.name == 'username' or field.name == 'email' or field.name == 'role' %}col-span-1 md:col-span-2{% endif %}" {% if field.name == 'subject' %}id="subject-wrapper"{% endif %}>
                        <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-gray-700 mb-1">
                            {{ field.label }}
                        </label>
                        {{ field }}
                        {% if field.errors %}
                            <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
                        {% endif %}
                        {% if field.help_text %}
                            <p class="mt-1 text-xs text-gray-500">{{ field.help_text|safe }}</p>
                        {% endif %}
                    </div>'''

new_div = '''                    {% if field.name == 'children' %}
                    <div id="children-wrapper" class="col-span-1 md:col-span-2" style="display: none;">
                        <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                        <div class="max-h-64 overflow-y-auto border border-gray-300 rounded-lg p-4 bg-white space-y-2">
                            {{ field }}
                        </div>
                        {% if field.errors %}
                            <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
                        {% endif %}
                        <p class="text-xs text-gray-500 mt-1">Check the boxes next to the students you want to link.</p>
                    </div>
                    {% else %}
                    <div class="{% if field.name == 'username' or field.name == 'email' or field.name == 'role' %}col-span-1 md:col-span-2{% endif %}" {% if field.name == 'subject' %}id="subject-wrapper"{% endif %}>
                        <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-gray-700 mb-1">
                            {{ field.label }}
                        </label>
                        {{ field }}
                        {% if field.errors %}
                            <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
                        {% endif %}
                        {% if field.help_text %}
                            <p class="mt-1 text-xs text-gray-500">{{ field.help_text|safe }}</p>
                        {% endif %}
                    </div>
                    {% endif %}'''

content = content.replace(old_div, new_div)

old_js = '''        const roleSelect = document.querySelector('select[name="role"]');
        const subjectWrapper = document.getElementById('subject-wrapper');
        const subjectInput = document.querySelector('select[name="subject"]');
        
        if (roleSelect && subjectWrapper) {
            function toggleSubject() {
                if (roleSelect.value === 'teacher') {
                    subjectWrapper.style.display = 'block';
                } else {
                    subjectWrapper.style.display = 'none';
                    if (subjectInput) {
                        subjectInput.value = '';
                    }
                }
            }
            
            toggleSubject();
            roleSelect.addEventListener('change', toggleSubject);
        }'''

new_js = '''        const roleSelect = document.querySelector('select[name="role"]');
        const subjectWrapper = document.getElementById('subject-wrapper');
        const subjectInput = document.querySelector('select[name="subject"]');
        const childrenWrapper = document.getElementById('children-wrapper');
        
        if (roleSelect) {
            function toggleFields() {
                if (subjectWrapper) {
                    if (roleSelect.value === 'teacher') {
                        subjectWrapper.style.display = 'block';
                    } else {
                        subjectWrapper.style.display = 'none';
                        if (subjectInput) subjectInput.value = '';
                    }
                }
                
                if (childrenWrapper) {
                    if (roleSelect.value === 'parent') {
                        childrenWrapper.style.display = 'block';
                    } else {
                        childrenWrapper.style.display = 'none';
                        const childrenCheckboxes = document.querySelectorAll('input[name="children"]');
                        if (childrenCheckboxes) {
                            childrenCheckboxes.forEach(cb => cb.checked = false);
                        }
                    }
                }
            }
            
            toggleFields();
            roleSelect.addEventListener('change', toggleFields);
        }'''

content = content.replace(old_js, new_js)

with open('templates/admin_portal/user_form.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated user_form.html correctly")
