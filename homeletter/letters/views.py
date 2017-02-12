from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from helpers.mixins import FormActionMessageMixin, OwnObjectMixin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib import messages
from django.db import transaction

from .models import Letter
from .forms import LetterForm
from category.models import Category


class LetterCreateView(LoginRequiredMixin, FormActionMessageMixin, View):
    template_name = "letters/letters-form.html"
    form_class = LetterForm

    def get(self, request, *args, **kwargs):
        form = LetterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LetterForm(request.POST)

        if form.is_valid():
            file = request.FILES['file'] if request.FILES else None
            letter = Letter()
            try:
                with transaction.atomic():
                    letter = Letter(
                        user=request.user,
                        date_created=datetime.now(),
                        favorite=0,
                        category=form.cleaned_data['category'],
                        note=form.cleaned_data['note'],
                        name=form.cleaned_data['name'],
                        date=form.cleaned_data['date'],
                        file=file
                    )
                    # update category in_use status
                    category = Category.objects.get(pk=letter.category.pk)
                    category.in_use = True
                    letter.save()
                    category.save()

                    messages.success(request, _('LETTER UPLOADED SUCCESSFULLY!!'))
                    return redirect('letters:index')
            except:
                messages.error(request, _('SOMETHING WENT WRONG, PLEASE TRY AGAIN LATER!'))
                if file is not None:
                    letter.file.delete()
                return redirect('letters:index')
        else:
            return render(request, self.template_name, {'form': form})

"""
# GENERIC CLASS BASED VIEW
# CANNOT DELETE UPLOADS WHEN EXCEPTION CAUGHT
class LetterCreateView(LoginRequiredMixin, FormActionMessageMixin, CreateView):
    template_name = "letters/letters-form.html"
    form_class = LetterForm

    success_msg = _("LETTER UPLOADED SUCCESSFULLY!")
    fail_msg = _('SOMETHING WENT WRONG, PLEASE TRY AGAIN LATER!')

    def form_valid(self, form):
        form.file = self.request.FILES['file'] if self.request.FILES else None  # no need to change the icon name
        # add extra fields
        form.instance.user = self.request.user
        form.instance.date_created = datetime.now()
        form.instance.favorite = 0
        return super(LetterCreateView, self).form_valid(form)
"""


class LetterIndexView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = 'letters/letters-index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        for l in qs:
            # get the favorite range
            if l.favorite >= 0:
                l.range1 = range(l.favorite)
                l.range2 = range(5 - l.favorite)
            # get the letter upload basename
            if l.file is not None:
                l.letter_name = l.file.name.split('/')[-1]
            else:
                l.letter_name = ""


        return qs


class LetterEditView(LoginRequiredMixin, OwnObjectMixin, FormActionMessageMixin, UpdateView):
    pass


class LetterDeleteView(LoginRequiredMixin, OwnObjectMixin, DeleteView):
    pass


class LetterDetailView(LoginRequiredMixin, DeleteView):
    pass