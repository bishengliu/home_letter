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
        view=views.RegisterView.as_view(),
        name='logout'
    ),
]