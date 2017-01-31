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
    )
]
