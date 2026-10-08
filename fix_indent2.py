lines = []
with open('accounts/forms.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('        children = forms.ModelMultipleChoiceField('):
        new_lines.append(line.replace('        children =', '    children ='))
    else:
        new_lines.append(line)

with open('accounts/forms.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
