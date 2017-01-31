from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=views.UpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^password$',
        view=views.PasswordView.as_view(),
        name='password'
    )
]