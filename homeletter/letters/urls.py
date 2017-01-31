from django.conf.urls import url
from . import views

urlpatterns = [
    # manage letter categories
    url(
        regex=r'^category$',
        view=views.CategoryListView.as_view(),
        name='list_category'
    ),
    url(
        regex=r'^add_category$',
        view=views.CategoryCreateView.as_view(),
        name='add_category'
    ),
    url(
        regex=r'^update_category/(?P<pk>\d+)/$',
        view=views.CategoryUpdateView.as_view(),
        name='update_category'
    ),
    url(
        regex=r'^delete_category/(?P<pk>\d+)/$',
        view=views.CategoryDeleteView.as_view(),
        name='delete_category'
    ),
    # manage letters
    url(
        regex=r'^$',
        view=views.LetterListView.as_view(),
        name='list_letter'
    ),
    url(
        regex=r'^add$',
        view=views.LetterCreateView.as_view(),
        name='add_letter'
    ),
    url(
        regex=r'^update/(?P<pk>\d+)/$',
        view=views.LetterUpdateView.as_view(),
        name='update_letter'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.LetterDeleteView.as_view(),
        name='delete_letter'
    )

]
