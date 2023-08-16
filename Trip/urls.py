"""
URL configuration for Trip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from journey.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page),
    path('profile/',profile_page , name="profile"),
    path('home/',trip_details , name="home"),
    path('login/',login_page , name="login_page"),
    path('logout/',logout_page , name="logout_page"),
    path('register/',register_page , name="register_page"),
    path('delete-trip/<id>/', delete_trip , name="delete_trip"),
    path('update-trip/<id>/', update_trip , name="update_trip"),
    path('leave/' , leave_update , name="leave"),
    path('download',download,name="download"),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

