from django import forms
from django.conf import settings
from .models import User, Profile
from django.utils.translation import ugettext_lazy as _
import re


# register form
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
    first_name = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=False, max_length=30), ),
        required=False,
        label=_("First Name"),
        error_message={'invalid': _("First Name contains only letters, numbers and underscores.")})
    last_name = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=False, max_length=30), ),
        required=False,
        label=_("Last Name"),
        error_message={'invalid': _("Last Name contains only letters, numbers and underscores.")})
    birth_date = forms.DateField(
        required=False,
        input_formats=settings.DATE_INPUT_FORMATS,
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
            if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
                msg = "The two password fields did not match."
                self.add_error('password1', _(msg))
                self.add_error('password2', _(msg))
                raise forms.ValidationError(_(msg))

            # strong password
            """
            password_pattern = re.compile("^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$")
            ^                         Start anchor
            (?=.*[A-Z])               Ensure string has one uppercase letter.
            (?=.*[!@#$&*])            Ensure string has one special case letter.
            (?=.*[0-9].*[0-9])        Ensure string has two digits.
            (?=.*[a-z].*[a-z].*[a-z]) Ensure string has three lowercase letters.
            .{8,8}                    Ensure string is of length at least 8.
            $                         End anchor.

            password_pattern = re.compile("^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$")
            (?=.*?\d) Checks for atleast one digit
            (?=.*?[A-Z]) Atleast one uppercsae.
            (?=.*?[a-z]) Atleast one lowercase.
            [A-Za-z\d]{10,} Matches uppercase or lowercase or digit characters 10 or more times. This ensures that the match must have atleast 10 characters.
            """
            password_pattern = re.compile("^(?=.*[A-Z])(?=.*[a-z].*[a-z])(?=.*[0-9].*[0-9]).{8,}$")
            isValid = re.match(password_pattern, self.cleaned_data.get('password1'))
            if not password_pattern.search(self.cleaned_data.get('password1')):
                msg = "Password contains at least: 1 uppercase letter, 2 lowcase letters, 2 digits and must be longer than 8 characters."
                self.add_error('password1', _(msg))
                # self.add_error('password2', _(msg))
                raise forms.ValidationError(_(msg))
        return self.cleaned_data


# login form
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
    # validation
    def clean_first_name(self):
        name_pattern=re.compile("^\w+$")
        is_valid = re.match(name_pattern, self.cleaned_data.get('first_name'))
        if not is_valid:
            msg = "First Name contains only letters, numbers and underscores."
            raise forms.ValidationError(_(msg))

    def clean_last_name(self):
        name_pattern=re.compile("^\w+$")
        is_valid = re.match(name_pattern, self.cleaned_data.get('last_name'))
        if not is_valid:
            msg = "Last Name contains only letters, numbers and underscores."
            raise forms.ValidationError(_(msg))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].required = True
        self.fields['birth_date'].input_formats=settings.DATE_INPUT_FORMATS

    class Meta:
        model = Profile
        fields = ('birth_date', 'photo')



















