from django.conf.urls import url
from . import views

urlpatterns = [
    # manage letter categories
    url(
        regex=r'^$',
        view=views.CategoryListView.as_view(),
        name='category'
    ),

    url(
        regex=r'^add_category$',
        view=views.CategoryCreateView.as_view(),
        name='add_category'
    ),
    # manage letters
]