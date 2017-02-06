# global mixins
from django.contrib import messages


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