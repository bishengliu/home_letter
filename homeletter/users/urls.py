from django.conf.urls import url
from . import views


urlpatterns = [

    # registration
    url(
        regex=r'^register$',
        view=views.RegisterView.as_view(),
        name='register'
    ),
    url(
        regex=r'^logout$',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        regex=r'^login$',
        view=views.LoginView.as_view(),
        name='login'
    ),
]