from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label = "Password")

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label = "Password")
    confirmpassword = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")
    email = forms.EmailField()