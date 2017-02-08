from django import forms
from homeletter.category.models import Category
from .models import Letter
from django.forms.widgets import Select


class LetterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)
        """
        self.fields['category'] = forms.ChoiceField(
            choices=[(c.id, c.name) for c in Category.objects.order_by('name').all()]
        )
        """

    def clean_favorite(self):
        pass

    class Meta:
        CHOICES = Category.objects.order_by('name').all()
        model = Letter
        fields = ("category", 'name', 'file', 'date', 'favorite', 'note')
        widgets = {
            'category': Select(choices=((c.id, c.name) for c in CHOICES)),
        }