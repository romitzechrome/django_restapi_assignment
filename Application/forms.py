from django import forms
from . import models
from .validators import validate_email, validate_course


class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class LoginForm(forms.Form):
    Username = forms.CharField(max_length=150)
    Password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['Username', 'Password']


class CourseModelForm(forms.ModelForm):
    Course = forms.CharField(validators=[validate_course])

    class Meta:
        model = models.Course
        fields = ['Course']


class AssigmentModelForm(forms.ModelForm):
    Deadline = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = models.Assigment
        fields = ['Name', 'Questions', 'Deadline']


class SolutionModelForm(forms.ModelForm):

    class Meta:
        model = models.Solution
        fields = ['title', 'answer', 'files']


class PointsCommentsModelForm(forms.ModelForm):
    class Meta:
        model = models.Solution
        fields = ['answer', 'points', 'comments']
