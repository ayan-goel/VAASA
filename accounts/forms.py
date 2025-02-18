from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ""
        return mark_safe(
            "".join(
                [
                    f'<div class="alert alert-danger" role="alert">{e}</div>'
                    for e in self
                ]
            )
        )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"class": "form-control"})
    )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "form-control"})
        self.fields["new_password2"].widget.attrs.update({"class": "form-control"})

