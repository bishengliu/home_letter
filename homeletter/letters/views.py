from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from homeletter.helpers.mixins import FormActionMessageMixin, OwnObjectMixin

#from .models import Letter
from .forms import LetterForm


# Create your views here.
class LetterCreateView(LoginRequiredMixin, FormActionMessageMixin, CreateView):
    template_name = "category/letters-form.html"
    form_class = LetterForm

"""
class LetterIndexView(LoginRequiredMixin, ListView):
    pass

class LetterEditView(LoginRequiredMixin, OwnObjectMixin, FormActionMessageMixin, UpdateView):
    pass


class LetterDeleteView(LoginRequiredMixin, OwnObjectMixin, DeleteView):
    pass
"""

