import re

with open('templates/admin_portal/user_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_wrapper = '''                    <div id="children-wrapper" class="col-span-1 md:col-span-2" style="display: none;">
                        <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                        <div class="max-h-64 overflow-y-auto border border-gray-300 rounded-lg p-4 bg-white space-y-2">
                            {{ field }}
                        </div>
                        {% if field.errors %}
                            <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
                        {% endif %}
                        <p class="text-xs text-gray-500 mt-1">Check the boxes next to the students you want to link.</p>
                    </div>'''

new_wrapper = '''                    <div id="children-wrapper" class="col-span-1 md:col-span-2" style="display: none;">
                        <label class="block text-sm font-medium text-gray-700 mb-2">{{ field.label }}</label>
                        
                        <!-- Search Box -->
                        <div class="mb-2">
                            <input type="text" id="student-search" placeholder="Search students by name..." class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-emerald-500 focus:border-emerald-500 outline-none transition">
                        </div>
                        
                        <!-- Checkboxes List -->
                        <div class="max-h-64 overflow-y-auto border border-gray-300 rounded-lg p-2 bg-white" id="student-list-container">
                            {% for checkbox in field %}
                            <div class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded transition-colors student-item">
                                {{ checkbox.tag }}
                                <label for="{{ checkbox.id_for_label }}" class="text-sm font-medium text-gray-700 cursor-pointer flex-1 select-none">
                                    {{ checkbox.choice_label }}
                                </label>
                            </div>
                            {% endfor %}
                        </div>
                        
                        {% if field.errors %}
                            <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
                        {% endif %}
                        <p class="text-xs text-gray-500 mt-2">Check the boxes next to the students you want to link.</p>
                    </div>'''

content = content.replace(old_wrapper, new_wrapper)

old_js = '''            toggleFields();
            roleSelect.addEventListener('change', toggleFields);
        }'''

new_js = '''            toggleFields();
            roleSelect.addEventListener('change', toggleFields);
        }
        
        // Student Search Logic
        const studentSearch = document.getElementById('student-search');
        if (studentSearch) {
            studentSearch.addEventListener('input', function(e) {
                const term = e.target.value.toLowerCase();
                const items = document.querySelectorAll('.student-item');
                items.forEach(item => {
                    const label = item.querySelector('label').textContent.toLowerCase();
                    if (label.includes(term)) {
                        item.style.display = 'flex';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        }'''

content = content.replace(old_js, new_js)

with open('templates/admin_portal/user_form.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated user_form.html with searchable checkboxes")
