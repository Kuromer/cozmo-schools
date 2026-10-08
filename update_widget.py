with open('accounts/forms.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_widget = "widget=forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 5}),"
new_widget = "widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500'}),"

content = content.replace(old_widget, new_widget)

with open('accounts/forms.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated accounts/forms.py")
