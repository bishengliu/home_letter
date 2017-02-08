from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from homeletter.helpers.mixins import FormActionMessageMixin, OwnObjectMixin


# Create your views here.
class LetterIndexView(LoginRequiredMixin, ListView):
    pass


class LetterCreateView(LoginRequiredMixin, FormActionMessageMixin, CreateView):
    pass


class LetterEditView(LoginRequiredMixin, OwnObjectMixin, FormActionMessageMixin, UpdateView):
    pass


class LetterDeleteView(LoginRequiredMixin, OwnObjectMixin, DeleteView):
    pass
