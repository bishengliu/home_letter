from django import forms
from .models import User, Profile
from django.utils.translation import ugettext_lazy as _
import re

#register form
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
        widget=forms.SelectDateWidget(attrs=dict(required=False), empty_label=("Year", "Month", "Day")),
        required=False,
        label=_("Birth Date"))
    photo = forms.ImageField(
        max_length=100,
        allow_empty_file=True,
        # help_text= _('Only allow for ".bmp", ".jpg", ".tiff" and ".png"!'),
        required=False,  # default True
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
        super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                msg = "The two password fields did not match."
                self.add_error('password1', _(msg))
                self.add_error('password2', _(msg))
                raise forms.ValidationError(_(msg))

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
                msg = "Password contains at least: 1 uppercase letter, 3 lowcase letters, 2 digits and must be longer than 8 characters."
                self.add_error('password1', _(msg))
                self.add_error('password2', _(msg))
                raise forms.ValidationError(_(msg))
        return self.cleaned_data

#login form
class LoginForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30), ),
        label=_("Username"))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False),),
        label=_("Password"))

    # validation
    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
            return self.cleaned_data['username']
        except User.DoesNotExist:
            raise forms.ValidationError(_('The username does not exist!'))

# for updating forms
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birth_date', 'photo')



















