from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime

from .models import Category
from .forms import CategoryForm

# mixin for message
class ActionMixin(object):

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ActionMixin, self).form_valid(form)


class CategoryCreateView(LoginRequiredMixin, ActionMixin, View):
    template_name = "category/create.html"
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        # validate user permission
        # user = request.user

        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            note = form.cleaned_data['note']
            icon = request.FILES['icon'] if request.FILES else None # no need to change the icon name
            try:
                Category.objects.create(
                    name=name,
                    icon=icon,
                    date=datetime.date(),
                    in_use=False,
                    user=user,
                    note=note
                )
                messages.success(request, _('Category Created!'))
                return render(request, self.template_name, {'form': form})
            except:
                messages.info(request, _('Something went wrong, please try again!'))
                if icon is not None:
                    icon.delete()
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})



