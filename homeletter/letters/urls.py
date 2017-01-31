from django.conf.urls import url
from . import views

urlpatterns = [
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
