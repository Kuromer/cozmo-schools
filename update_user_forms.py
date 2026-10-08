import re

# 1. Update accounts/forms.py
with open('accounts/forms.py', 'r', encoding='utf-8') as f:
    forms_py = f.read()

# Add children field to CustomUserCreationForm
creation_field = '''    children = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 5}),
        required=False,
        label='Linked Students (For Parents only)'
    )
    
    class Meta(UserCreationForm.Meta):'''

forms_py = forms_py.replace('class Meta(UserCreationForm.Meta):', creation_field)

creation_init = '''        self.fields['email'].required = True
        
        from school.models import Student
        self.fields['children'].queryset = Student.objects.all()'''
forms_py = forms_py.replace("self.fields['email'].required = True", creation_init, 1)

creation_save = '''    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.role == 'parent':
                selected_students = self.cleaned_data.get('children', [])
                for student in selected_students:
                    student.parent = user
                    student.save()
        return user'''
forms_py = forms_py.replace("return cleaned_data", "return cleaned_data\n\n" + creation_save, 1)


# Add children field to CustomUserChangeForm
change_field = '''    children = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 5}),
        required=False,
        label='Linked Students (For Parents only)'
    )
    
    class Meta:'''
forms_py = forms_py.replace('class Meta:', change_field)

change_init = '''        self.fields['email'].required = True
        
        from school.models import Student
        self.fields['children'].queryset = Student.objects.all()
        if self.instance and self.instance.pk and self.instance.role == 'parent':
            self.fields['children'].initial = self.instance.children.all()'''
forms_py = forms_py.replace("self.fields['email'].required = True", change_init, 1)

change_save = '''    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.role == 'parent':
                selected_students = self.cleaned_data.get('children', [])
                from school.models import Student
                Student.objects.filter(parent=user).exclude(id__in=[s.id for s in selected_students]).update(parent=None)
                for student in selected_students:
                    student.parent = user
                    student.save()
        return user'''
forms_py = forms_py.replace("return cleaned_data", "return cleaned_data\n\n" + change_save, 1)

with open('accounts/forms.py', 'w', encoding='utf-8') as f:
    f.write(forms_py)

print("Updated accounts/forms.py")
