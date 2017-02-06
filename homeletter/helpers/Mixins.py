# global mixins
from django.contrib import messages
from django.http import Http404


# mixin for message
class FormActionMessageMixin(object):

    @property
    def success_msg(self):
        return NotImplemented

    @property
    def fail_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FormActionMessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, self.fail_msg)
        return super(FormActionMessageMixin, self).form_invalid(form)


# mixin for only allow modify/deleting own letters and categories
class OwnObjectMixin(object):

    def get_object(self, queryset=None):
        obj = super(OwnObjectMixin, self).get_object()
        if self.request.user.pk != obj.user.id:
            raise Http404
        return obj
