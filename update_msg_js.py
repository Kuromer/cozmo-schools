import os

js_script = '''
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const parentSelect = document.getElementById('id_recipient');
        const studentSelect = document.getElementById('id_student');
        
        if (!parentSelect || !studentSelect) return;
        
        // Save the original options
        const allOptions = Array.from(studentSelect.options);
        
        function filterStudents() {
            const parentId = parentSelect.value;
            const currentSelected = studentSelect.value;
            
            // Clear current options
            studentSelect.innerHTML = '';
            
            let hasValidSelection = false;
            
            allOptions.forEach(option => {
                const optParentId = option.getAttribute('data-parent-id');
                if (!option.value || optParentId === parentId) {
                    studentSelect.appendChild(option.cloneNode(true));
                    if (option.value === currentSelected) {
                        hasValidSelection = true;
                    }
                }
            });
            
            if (hasValidSelection) {
                studentSelect.value = currentSelected;
            } else {
                studentSelect.value = '';
            }
        }
        
        parentSelect.addEventListener('change', filterStudents);
        filterStudents();
    });
</script>
{% endblock %}'''

with open('templates/teacher_portal/message_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'filterStudents' not in content:
    content = content.replace('{% endblock %}', js_script)
    with open('templates/teacher_portal/message_form.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated teacher message_form.html")
