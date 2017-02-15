"""homeletter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views

# import views from users app
from users import views as users_view
from home import views as home_view

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # home app
    url(r'^$', include('home.urls', namespace="home")),

    # User management
    url(r'^user/', include('users.urls', namespace="users")),

    # register
    url(
        regex=r'^register$',
        view=users_view.RegisterView.as_view(),
        name='register'
    ),
    # logout
    url(
        regex=r'^logout$',
        view=users_view.LogoutView.as_view(),
        name='logout'
    ),
    # login
    url(
        regex=r'^login$',
        view=users_view.LoginView.as_view(),
        name='login'
    ),
    # CATEGORY MANAGEMENT
    url(r'^category/', include('category.urls', namespace="category")),
    # LETTER MANAGEMENT
    url(r'^letter/', include('letters.urls', namespace="letters"))


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# allow to serve static media files during development


# for viewing these pages when DEBUG is true
if settings.DEBUG:

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
