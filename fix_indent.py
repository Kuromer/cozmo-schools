with open('accounts/forms.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('accounts/forms.py', 'w', encoding='utf-8') as f:
    for line in lines:
        if line.startswith('    class Meta(UserCreationForm.Meta):'):
            f.write(line)
        elif line.startswith('class Meta(UserCreationForm.Meta):'):
            f.write('    ' + line)
        elif line.startswith('    class Meta:'):
            f.write(line)
        elif line.startswith('class Meta:'):
            f.write('    ' + line)
        else:
            f.write(line)
