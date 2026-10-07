from django import forms
from .models import Student, SchoolClass, Fee, Warning, ParentInvitation, Homework, Evaluation, Attendance, Message
from accounts.models import CustomUser

# Common Tailwind CSS classes for form widgets
INPUT_CLASS = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition text-sm'
SELECT_CLASS = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition text-sm bg-white'
TEXTAREA_CLASS = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition text-sm'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'parent', 'grade_level']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'parent': forms.Select(attrs={'class': SELECT_CLASS}),
            'grade_level': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g., Grade 5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = CustomUser.objects.filter(role='parent')
        self.fields['parent'].empty_label = '-- Select Parent --'

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'amount', 'description', 'due_date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': SELECT_CLASS}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Amount', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Fee Description'}),
            'due_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'status': forms.Select(attrs={'class': SELECT_CLASS}),
        }

class WarningForm(forms.ModelForm):
    class Meta:
        model = Warning
        fields = ['student', 'warning_type', 'reason']
        widgets = {
            'student': forms.Select(attrs={'class': SELECT_CLASS}),
            'warning_type': forms.Select(attrs={'class': SELECT_CLASS}),
            'reason': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Reason for warning...'}),
        }

class CancelWarningForm(forms.Form):
    cancellation_reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3, 'placeholder': 'Reason for cancellation...'}),
        required=True
    )

class ParentInvitationForm(forms.ModelForm):
    class Meta:
        model = ParentInvitation
        fields = ['parent', 'student', 'date', 'time', 'invitation_type', 'status', 'notes']
        widgets = {
            'parent': forms.Select(attrs={'class': SELECT_CLASS}),
            'student': forms.Select(attrs={'class': SELECT_CLASS}),
            'date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': INPUT_CLASS, 'type': 'time'}),
            'invitation_type': forms.Select(attrs={'class': SELECT_CLASS}),
            'status': forms.Select(attrs={'class': SELECT_CLASS}),
            'notes': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3, 'placeholder': 'Notes...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = CustomUser.objects.filter(role='parent')

class InvitationUpdateForm(forms.ModelForm):
    class Meta:
        model = ParentInvitation
        fields = ['status', 'date', 'time', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': SELECT_CLASS}),
            'date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': INPUT_CLASS, 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
        }

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['school_class', 'title', 'content', 'due_date']
        widgets = {
            'school_class': forms.Select(attrs={'class': SELECT_CLASS}),
            'title': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Homework Title'}),
            'content': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 5, 'placeholder': 'Homework details...'}),
            'due_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['school_class'].queryset = SchoolClass.objects.filter(teachers=teacher)

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['student', 'subject', 'grade', 'comment']
        widgets = {
            'student': forms.Select(attrs={'class': SELECT_CLASS}),
            'subject': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Subject'}),
            'grade': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Grade (e.g., A+, 95%)'}),
            'comment': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Evaluation comments...'}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            classes = SchoolClass.objects.filter(teachers=teacher)
            student_ids = Student.objects.filter(classes__in=classes).values_list('id', flat=True).distinct()
            self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'student', 'subject', 'content']
        widgets = {
            'recipient': forms.Select(attrs={'class': SELECT_CLASS}),
            'student': forms.Select(attrs={'class': SELECT_CLASS}),
            'subject': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Message Subject'}),
            'content': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 5, 'placeholder': 'Message content...'}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = CustomUser.objects.filter(role='parent')
        self.fields['recipient'].label = 'Parent'
        if teacher:
            classes = SchoolClass.objects.filter(teachers=teacher)
            student_ids = Student.objects.filter(classes__in=classes).values_list('id', flat=True).distinct()
            self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)
