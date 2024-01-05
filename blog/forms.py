from dataclasses import fields
from unicodedata import name
from xml.dom.minidom import Attr
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UpdatePost, Profile

class SignUpForm(UserCreationForm):

    field_order = ("first_name", "last_name", "username",
                   "email", "password1", "password2")

    username = forms.CharField(label='Username',
                               min_length=5, max_length=160,
                               error_messages={'required': 'Invalid username'},
                               widget=forms.TextInput(attrs={'placeholder': 'Choose A Username'}))

    email = forms.EmailField(label='Email',
                             error_messages={'required': 'invalid email'},
                             widget=forms.TextInput(
                                 attrs={"placeholder": 'Your Email'}),
                             min_length=11)

    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'placeholder': "Your first name"}))
    last_name = forms.CharField(
        label="Last/other Name", widget=forms.TextInput(attrs={'placeholder': "Your other names"}))

    password1 = forms.CharField(label='Password',

                                widget=forms.PasswordInput(
                                    attrs={'placeholder': "must be a number and alphabet"}),
                                error_messages={
                                    "required": "check {} and try again".format('password')}
                                )

    password2 = forms.CharField(label='Confirm(Password)',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': "Re-type your password here"}),
                                )

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("username already exit")
        return username

    def lastname_clean(self):
        lastname = self.cleaned_data['last_name'].lower()
        return lastname

    def firstname_clean(self):
        firstname = self.cleaned_data['first_name'].lower()
        return firstname

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("email already exit")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("password does not match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(username=self.username_clean(),
                                        email=self.email_clean(),
                                        first_name=self.firstname_clean(),
                                        last_name=self.lastname_clean(),
                                        password=self.clean_password2(),
                                        )
        return user


class loginform(forms.Form):
    username = forms.CharField(
        label="Username",
        show_hidden_initial=True,
        error_messages={"required": "please login"},
        widget=forms.TextInput(attrs={'placeholder': 'Your username'}))

    password = forms.CharField(
        label="Password",

        error_messages={"required": "incorect password"},
        widget=forms.PasswordInput(attrs={"placeholder": "your password"})


    )

    def clean_username(self):
        email = self.cleaned_data["email"]

        if email.count() is None:
            raise ValidationError("input a name to continue")
        else:
            emails = email.lower()

class UpdateForm(forms.ModelForm):
        class Meta:
            model =UpdatePost
            fields = ["title","catgories","image", "discriptions", ]
            widgets = {
                "title":forms.TextInput(
                    attrs={"placeholder":"Title here"}
                ),
                "discriptions": forms.CharField(widget=forms.Textarea(attrs={'class': 'ckeditor'}))
            }
