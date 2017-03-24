from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from letters.models import Letter


# generate pdf tb
# http://www.yaconiello.com/blog/auto-generating-pdf-covers/
class HomeIndexView(View):
    template_name = "home/home-index.html"

    def get(self, request, *args, **kwargs):
        letters = Letter.objects.order_by('-date')[:20]
        for l in letters:
            # get the favorite range
            if l.favorite >= 0:
                l.range1 = range(l.favorite)
                l.range2 = range(5 - l.favorite)
            # get the letter upload basename
            if l.file is not None:
                l.letter_name = l.file.name.split('/')[-1]
            else:
                l.letter_name = ""
        return render(request, self.template_name, {'letters': letters})
