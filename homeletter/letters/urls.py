from django.conf.urls import url
from . import views


"""url(
        regex=r'^$',
        view=views.LetterIndexView.as_view(),
        name='index'
    ),

"""

urlpatterns = [

    url(
        regex=r'^$',
        view=views.LetterIndexView.as_view(),
        name='index'
    ),

    url(
        regex=r'^create$',
        view=views.LetterCreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^edit/(?P<pk>\d+)/$',
        view=views.LetterEditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.LetterDeleteView.as_view(),
        name='delete'
    ),
url(
        regex=r'^detail/(?P<pk>\d+)/$',
        view=views.LetterDetailView.as_view(),
        name='detail'
    ),
]
