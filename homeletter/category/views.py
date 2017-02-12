from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView
from datetime import datetime
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404

from helpers.mixins import FormActionMessageMixin, OwnObjectMixin
from .models import Category
from .forms import CategoryForm
from letters.models import Letter


class CategoryCreateView(LoginRequiredMixin, View):
    template_name = "category/category-form.html"
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            note = form.cleaned_data['note']
            icon = request.FILES['icon'] if request.FILES else None # no need to change the icon name
            category = Category()
            try:
                category = Category.objects.create(
                    name=name,
                    icon=icon,
                    date=datetime.now(),
                    in_use=False,
                    user=user,
                    note=note
                )
                messages.success(request, _('Category Created!'))
                return redirect('category:index')
            except:
                messages.error(request, _('Something went wrong, please try again!'))
                if icon is not None:
                    category.icon.delete()
                return redirect('category:index')
        else:
            return render(request, self.template_name, {'form': form})


class CategoryEditView(LoginRequiredMixin, OwnObjectMixin, FormActionMessageMixin, UpdateView):
    # validate user permission using mixin
    template_name = "category/category-form.html"
    form_class = CategoryForm
    model = Category

    success_msg = _("CATEGORY UPDATED SUCCESSFULLY!")
    fail_msg = _('SOMETHING WENT WRONG, PLEASE TRY AGAIN LATER!')

    def form_valid(self, form):
        form.icon = self.request.FILES['icon'] if self.request.FILES else None
        return super(CategoryEditView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category/category-index.html"


class CategoryDeleteView(LoginRequiredMixin, OwnObjectMixin, DeleteView):
    model = Category
    template_name = "category/category-delete.html"
    success_message = _("CATEGORY DELETED SUCCESSFULLY!")
    failed_message = _("CATEGORY NOT DELETED, PLEASE TRY AGAIN LATER!")
    success_url = reverse_lazy('category:index')

    def get_object(self, queryset=None):
        obj = super(CategoryDeleteView, self).get_object()
        if obj.in_use:
            raise Http404
        letters = Letter.objects.filter(category_id=obj.pk)
        if letters.count() > 0:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        # get the object
        obj = get_object_or_404(Category, pk=kwargs['pk'])
        try:
            # delete icon
            if obj.icon:
                obj.icon.delete()
            # delete the object
            obj.delete()
            messages.success(request, self.success_message)
        except:
            messages.error(request, self.failed_message_message)
        return redirect("category:index")
