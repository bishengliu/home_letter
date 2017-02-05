from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView
from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404


from .models import Category
from .forms import CategoryForm


# mixin for message
class ActionMixin(object):

    @property
    def success_msg(self):
        return NotImplemented

    @property
    def fail_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, self.fail_msg)
        return super(ActionMixin, self).form_invalid(form)


class CategoryCreateView(LoginRequiredMixin, View):
    # validate user permission using mixin
    template_name = "category/form.html"
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
                messages.info(request, _('Something went wrong, please try again!'))
                if icon is not None:
                    category.icon.delete()
                return redirect('category:index')
        else:
            return render(request, self.template_name, {'form': form})


class CategoryEditView(LoginRequiredMixin, ActionMixin, UpdateView):
    # validate user permission using mixin
    template_name = "category/form.html"
    form_class = CategoryForm
    model = Category

    success_msg = _("Category Updated Successfully!")
    fail_msg = _('Something went wrong, please try again later!')

    def form_valid(self, form):
        form.icon = self.request.FILES['icon'] if self.request.FILES else None # no need to change the icon name
        return super(CategoryEditView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category/index.html"


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category/delete.html"
    success_message = _("Category Deleted Successfully!")
    success_url = reverse_lazy('category:index')

    def get_object(self, queryset=None):
        obj = super(CategoryDeleteView, self).get_object()
        if obj.in_use:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        super(CategoryDeleteView, self).delete(request, *args, **kwargs)


"""
        self.object = get_object_or_404(Category, pk=kwargs['pk'])
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
"""


