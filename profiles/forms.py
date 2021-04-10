from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, \
    SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')