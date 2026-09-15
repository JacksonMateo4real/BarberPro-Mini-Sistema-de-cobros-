from django import forms
from accounts.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



class CreateEmployeeForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        required=True,
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        required=True,
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    role = forms.ChoiceField(
        required=True,
        choices=[
            ('owner', 'Owner'),
            ('barber', 'Barber')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']

class UpdateEmployeeForm(forms.ModelForm):
    selected_employee_id = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label='Empleado',
    )

    username = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        required=False,
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        required=False,
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    phone_number = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    role = forms.ChoiceField(
        required=False,
        choices=[
            ('owner', 'Owner'),
            ('barber', 'Barber')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'role']
