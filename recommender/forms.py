from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    goto = forms.ChoiceField(label="Go To", choices=(
            ('D', 'demo'),
            ('M', 'main page')
        )
    )

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    goto = forms.ChoiceField(
        choices=(
            ('D', 'demo'),
            ('M', 'main page')
        ),
        label="Go To"
    )
