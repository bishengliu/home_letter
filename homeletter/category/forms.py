from django import forms
from django.utils.translation import ugettext_lazy as _
import re
from .models import Category


class CategoryForm(forms.ModelForm):

    def clean_name(self):
        name_pattern = re.compile("^\w+$")
        is_valid = re.match(name_pattern, self.cleaned_data.get('name'))
        # validate name
        if not is_valid:
            msg = "Name contains only letters, numbers and underscores!"
            raise forms.ValidationError(_(msg))
        return self.cleaned_data['name']

    class Meta:
        model = Category
        fields = ("name", 'icon', 'note')
