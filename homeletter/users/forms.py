from django import forms
from .models import User, Profile
from django.utils.translation import ugettext_lazy as _
import re


class RegistrationForm(forms.Form):

    # fields
    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30),),
        label=_("Username"),
        error_message={'invalid': _("Username contains only letters, numbers and underscores.")})
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=30),),
        label=_("Email"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False),),
        label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False),),
        label=_("Password (again)"))
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs=dict(required=True), empty_label=("Year", "Month", "Day")),
        label=_("Birth Date"))
    photo = forms.ImageField(
        max_length=100,
        allow_empty_file=True,
        label=_("Photo"))

    # validation
    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_('The username already exists. Please try another one.'))

    # validate email
    def clean_email(self):
        try:
            User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_('The email already taken. Please try another one.'))

    # validate password1/2
    def clean(self):
        if 'password1' in self.cleaned_data['password1'] and 'password2' in self.cleaned_data['password2']:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))

            # strong password
            """
            password_pattern = re.compile("^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$")
            ^                         Start anchor
            (?=.*[A-Z])               Ensure string has one uppercase letter.
            (?=.*[!@#$&*])            Ensure string has one special case letter.
            (?=.*[0-9].*[0-9])        Ensure string has two digits.
            (?=.*[a-z].*[a-z].*[a-z]) Ensure string has three lowercase letters.
            .{8}                      Ensure string is of length 8.
            $                         End anchor.
            """
            password_pattern = re.compile("^(?=.*[A-Z])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$")
            if not password_pattern.match(self.cleaned_data['password1']):
                raise forms.ValidationError(_("Password contains at least: 1 uppercase letter, 3 lowcase letters, 2 digits and must be longer than 8 characters"))
        return self.cleaned_data


# for updating forms
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birth_date', 'photo')



















