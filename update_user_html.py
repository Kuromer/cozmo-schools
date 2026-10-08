with open('templates/admin_portal/user_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the children field display togglable based on role == 'parent'

# In the form loop, wrap the children field
wrap_old = '''{% if field.name == 'subject' %}
                <div id="subject_wrapper" style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                    {{ field }}
                    {% if field.help_text %}<p class="text-xs text-gray-500 mt-1">{{ field.help_text }}</p>{% endif %}
                </div>
            {% else %}'''

wrap_new = '''{% if field.name == 'subject' %}
                <div id="subject_wrapper" style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                    {{ field }}
                    {% if field.help_text %}<p class="text-xs text-gray-500 mt-1">{{ field.help_text }}</p>{% endif %}
                </div>
            {% elif field.name == 'children' %}
                <div id="children_wrapper" style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                    {{ field }}
                    <p class="text-xs text-gray-500 mt-1">Hold Ctrl (or Cmd) to select multiple students.</p>
                </div>
            {% else %}'''

content = content.replace(wrap_old, wrap_new)

# Update the JS block
js_old = '''        const roleSelect = document.querySelector('select[name="role"]');
        const subjectWrapper = document.getElementById('subject_wrapper');
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
            }'''

js_new = '''        const roleSelect = document.querySelector('select[name="role"]');
        const subjectWrapper = document.getElementById('subject_wrapper');
        const subjectInput = document.querySelector('select[name="subject"]');
        const childrenWrapper = document.getElementById('children_wrapper');
        const childrenInput = document.querySelector('select[name="children"]');
        
        if (roleSelect) {
            function toggleSubject() {
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
                        if (childrenInput) {
                            Array.from(childrenInput.options).forEach(opt => opt.selected = false);
                        }
                    }
                }
            }'''

content = content.replace(js_old, js_new)

with open('templates/admin_portal/user_form.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated user_form.html")
