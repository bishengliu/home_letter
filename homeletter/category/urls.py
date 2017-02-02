from django.conf.urls import url
from . import views

urlpatterns = [
    # manage letter categories
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'
    ),
    url(
        regex=r'^create$',
        view=views.CreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^edit/(?P<pk>\d+)/$',
        view=views.EditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.DeleteView.as_view(),
        name='delete'
    )
]
