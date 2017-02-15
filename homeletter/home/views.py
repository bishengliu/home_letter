from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class HomeIndexView(View):
    template_name = "home/home-index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
