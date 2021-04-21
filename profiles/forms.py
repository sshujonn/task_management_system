import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, \
    SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from profiles.models import Profile


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.First Name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.Last Name.')
    email = forms.EmailField(max_length=254, help_text='Required. This will be used as the username.')
    password1 = forms.CharField(help_text='Password must contain at least 8 characters with the combination of letters, numbers.')
    password2 = forms.CharField(help_text='Please confirm your password again')


    designation = ChoiceFieldNoValidation(
        choices=Profile.DesignationChoices.choices,
    )

    salutation = ChoiceFieldNoValidation(
        choices=Profile.SalutationChoices.choices,
    )


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2 or len(first_name) > 16:
            raise forms.ValidationError("First Name should be between 2 - 16 charecter")

        if bool(re.search('[\d\s]',first_name)): #firstname should not have whitespace or digits
            raise forms.ValidationError("Please dont use numbers or space in First Name Field")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2 or len(last_name) > 16:
            raise forms.ValidationError("Last Name should be between 2 - 16 charecter")

        if bool(re.search('[\d\s]',last_name)): #lastname should not have whitespace or digits
            raise forms.ValidationError("Please dont use numbers or space in Last Name Field")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        # import pdb;pdb.set_trace()
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Another User with this email already exists.')
        return email

    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        # import pdb;pdb.set_trace()
        if designation and str(designation) in dict(Profile.DesignationChoices.choices):
            return designation
        else:
            raise forms.ValidationError(u'Invalid Designation Choice.')


    def clean_salutation(self):
        salutation = self.cleaned_data.get('salutation')

        if salutation and str(salutation) in dict(Profile.SalutationChoices.choices):
            return salutation
        else:
            raise forms.ValidationError(u'Invalid Salutation Choice.')

    class Meta:
        model = Profile
        fields = ( 'email', 'first_name', 'last_name', 'salutation', 'designation', 'password1', 'password2', )

