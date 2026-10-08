from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser

INPUT_CLASS = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition text-sm'
SELECT_CLASS = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition text-sm bg-white'

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition',
            'placeholder': 'Password'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    children = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500'}),
        required=False,
        label='Linked Students (For Parents only)'
    )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'subject')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': SELECT_CLASS})
            else:
                field.widget.attrs.update({'class': INPUT_CLASS})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        from school.models import Student
        self.fields['children'].queryset = Student.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role != 'teacher':
            cleaned_data['subject'] = ''
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.role == 'parent':
                selected_students = self.cleaned_data.get('children', [])
                for student in selected_students:
                    student.parent = user
                    student.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    password = None
    children = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500'}),
        required=False,
        label='Linked Students (For Parents only)'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'subject', 'is_active')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': SELECT_CLASS})
            elif not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': INPUT_CLASS})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        from school.models import Student
        self.fields['children'].queryset = Student.objects.all()
        if self.instance and self.instance.pk and self.instance.role == 'parent':
            self.fields['children'].initial = self.instance.children.all()

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role != 'teacher':
            cleaned_data['subject'] = ''
        return cleaned_data

    def save(self, commit=True):
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
        return user