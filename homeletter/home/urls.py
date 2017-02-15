from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.HomeIndexView.as_view(),
        name='index'
    )
]