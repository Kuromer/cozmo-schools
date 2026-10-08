import re

with open('school/forms.py', 'r', encoding='utf-8') as f:
    forms_py = f.read()

student_select_class = '''
class StudentSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value:
            try:
                student = Student.objects.get(pk=value.value)
                option['attrs']['data-parent-id'] = student.parent_id
            except Exception:
                pass
        return option
'''

if 'class StudentSelect' not in forms_py:
    # insert it after constants
    pattern = r"(TEXTAREA_CLASS = '.*?')"
    forms_py = re.sub(pattern, r'\1\n' + student_select_class, forms_py, count=1)

# replace forms.Select with StudentSelect for student field in ParentInvitationForm
# Find class ParentInvitationForm and replace student widget
pif_pattern = r"(class ParentInvitationForm.*?\'student\': )forms\.Select(\(attrs=\{.*?\}\),)"
forms_py = re.sub(pif_pattern, r'\1StudentSelect\2', forms_py, flags=re.DOTALL)

# replace forms.Select with StudentSelect for student field in MessageForm
mf_pattern = r"(class MessageForm.*?\'student\': )forms\.Select(\(attrs=\{.*?\}\),)"
forms_py = re.sub(mf_pattern, r'\1StudentSelect\2', forms_py, flags=re.DOTALL)

with open('school/forms.py', 'w', encoding='utf-8') as f:
    f.write(forms_py)

print("Updated forms.py")
