from django.conf.urls import url
from . import views
'''
url(
        regex=r'^edit/(?P<pk>\d+)/$',
        view=views.EditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.DeleteView.as_view(),
        name='delete'
    ),
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'
    ),
'''
urlpatterns = [

    url(
        regex=r'^create$',
        view=views.CategoryCreateView.as_view(),
        name='create'
    ),

]
