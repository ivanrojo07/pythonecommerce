from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Nombre completo",
                "id":"form_full_name"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Tu correo electronico'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Contenido',

            }
        ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "gmail.com" in email:
            raise forms.ValidationError('Email has to be a gmail.com')
        return email

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":"Nombre de usuario",
            "id":"form_username"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class":"form-control",
            "placeholder":"Contraseña",
            "id":"form_password"
        },
        render_value=True))
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":"Nombre de usuario",
            "id":"form_username"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={
                "class":"form-control",
                "placeholder":"Correo Electronico",
                "id":"form_email"
            }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class":"form-control",
            "placeholder":"Contraseña",
            "id":"form_password"
        },
        render_value=True))
    password2 = forms.CharField(label="Password confirm",widget=forms.PasswordInput(
        attrs={
            "class":"form-control",
            "placeholder":"Contraseña",
            "id":"form_password"
        },
        render_value=True))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('Username is taken')
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email is taken')
        return email
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError('Passwords must match')
        return data