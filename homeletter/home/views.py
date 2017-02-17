from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from letters.models import Letter


# generate pdf tb
# http://www.yaconiello.com/blog/auto-generating-pdf-covers/
class HomeIndexView(View):
    template_name = "home/home-index.html"

    def get(self, request, *args, **kwargs):
        letters = Letter.objects.order_by('date')[:2]
        return render(request, self.template_name, {'letters': letters})
