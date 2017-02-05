from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.CategoryListView.as_view(),
        name='index'
    ),
    url(
        regex=r'^create$',
        view=views.CategoryCreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^edit/(?P<pk>\d+)/$',
        view=views.CategoryEditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.CategoryDeleteView.as_view(),
        name='delete'
    )
]
