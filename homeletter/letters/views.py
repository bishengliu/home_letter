from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DeleteView
from helpers.mixins import FormActionMessageMixin, OwnObjectMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib import messages
from django.db import transaction
import json
import os

from .models import Letter
from .forms import LetterForm
from category.models import Category


class LetterCreateView(LoginRequiredMixin, FormActionMessageMixin, View):
    template_name = "letters/letters-form.html"
    form_class = LetterForm

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('category_pk', None)
        if param is not None:
            form = LetterForm()
            return render(request, self.template_name, {'form': form, 'category_pk': int(param)})
        else:
            form = LetterForm()
            return render(request, self.template_name, {'form': form })

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


class LetterIndexView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = 'letters/letters-index.html'
    category_pk = None

    def get_queryset(self):
        p = self.kwargs.get('category_id', None)
        if p is not None and int(p) > 0:
            self.queryset = Letter.objects.filter(category_id__exact=int(p))
            self.category_pk = int(p)
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


class LetterEditView(LoginRequiredMixin, View):
    template_name = "letters/letters-form.html"
    form_class = LetterForm

    def get(self, request, *args, **kwargs):
        letter = get_object_or_404(Letter, pk=kwargs['pk'])
        letter_name = letter.file.name.split('/')[-1]
        form = LetterForm(instance=letter)
        return render(request, self.template_name, {'form': form, 'letter_name': letter_name})

    def post(self, request, *args, **kwargs):
        form = LetterForm(request.POST)
        letter = get_object_or_404(Letter, pk=kwargs['pk'])
        if form.is_valid():
            file = request.FILES['file'] if request.FILES else None
            try:
                letter.category=form.cleaned_data['category']
                letter.date = form.cleaned_data['date']
                letter.name = form.cleaned_data['name']
                letter.note = form.cleaned_data['note']
                if file is not None:
                    if letter.file and os.path.isfile(letter.file.url):
                        letter.file.delete()
                    letter.file = file
                letter.save()

                messages.success(request, _('LETTER UPDATED SUCCESSFULLY!!'))
                return redirect('letters:index')
            except:
                messages.error(request, _('SOMETHING WENT WRONG, PLEASE TRY AGAIN LATER!'))
                return redirect('letters:index')
        else:
            return render(request, self.template_name, {'form': form})


class LetterDeleteView(LoginRequiredMixin, OwnObjectMixin, DeleteView):
    model = Letter
    template_name = "letters/letters-delete.html"
    success_message = _("LETTER DELETED SUCCESSFULLY!")
    failed_message = _("LETTER NOT DELETED, PLEASE TRY AGAIN LATER!")
    success_url = reverse_lazy('letters:index')

    def get_object(self, queryset=None):
        obj = super(LetterDeleteView, self).get_object()
        if obj.favorite >= 0:
            obj.range1 = range(obj.favorite)
            obj.range2 = range(5 - obj.favorite)
        # get the letter upload basename
        if obj.file is not None:
            obj.letter_name = obj.file.name.split('/')[-1]
        else:
            obj.letter_name = ""
        return obj

    def delete(self, request, *args, **kwargs):
        # get the object
        letter = get_object_or_404(Letter, pk=kwargs['pk'])
        try:
            # delete file
            if letter.file and os.path.isfile(letter.file.url):
                letter.file.delete()
            letter.delete()
            messages.success(request, self.success_message)
        except:
            messages.error(request, self.failed_message)
        return redirect("letters:index")


# ajax call
class LetterFavoriteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            data = request.GET['favorite']
            obj = json.loads(data)
            fav = obj['fav']
            pk = obj['pk']
            # get the letter
            letter = Letter.objects.get(pk=pk)
            letter .favorite = fav
            letter.save()

            # return json res
            return JsonResponse({'status': 'success'}, safe=False)
        except:
            return JsonResponse({'status': 'failure'}, safe=False)
