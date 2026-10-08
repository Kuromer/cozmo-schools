with open('templates/admin_portal/user_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''            {% elif field.name == 'children' %}
                <div id="children_wrapper" style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                    {{ field }}
                    <p class="text-xs text-gray-500 mt-1">Hold Ctrl (or Cmd) to select multiple students.</p>
                </div>'''

new_block = '''            {% elif field.name == 'children' %}
                <div id="children_wrapper" style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                    <div class="max-h-64 overflow-y-auto border border-gray-300 rounded-lg p-4 bg-white space-y-2">
                        {{ field }}
                    </div>
                    <p class="text-xs text-gray-500 mt-1">Check the boxes next to the students you want to link.</p>
                </div>'''

content = content.replace(old_block, new_block)

# Update Javascript: childrenInput shouldn't unselect since it's checkboxes now.
# Wait, if we hide it, we might want to uncheck all checkboxes.
# childrenInput = document.querySelector('select[name="children"]'); this will be null for checkboxes.
js_old = '''                        if (childrenInput) {
                            Array.from(childrenInput.options).forEach(opt => opt.selected = false);
                        }'''

js_new = '''                        const childrenCheckboxes = document.querySelectorAll('input[name="children"]');
                        if (childrenCheckboxes) {
                            childrenCheckboxes.forEach(cb => cb.checked = false);
                        }'''

content = content.replace(js_old, js_new)

with open('templates/admin_portal/user_form.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated user_form.html")
