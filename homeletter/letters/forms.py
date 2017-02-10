from django import forms
from django.forms.widgets import Select

from category.models import Category
from .models import Letter

class LetterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)
        """
        self.fields['category'] = forms.ChoiceField(
            choices=[(c.id, c.name) for c in Category.objects.order_by('name').all()]
        )
        """

        self.fields['category'].empty_label = "PLEASE SELECT ..."


    class Meta:
        CHOICES = Category.objects.order_by('name').all()
        model = Letter
        fields = ("category", 'name', 'file', 'date', 'note')
        widgets = {
            'category': Select(choices=((c.id, c.name) for c in CHOICES)),
        }

