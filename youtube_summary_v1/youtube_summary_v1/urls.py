"""
URL configuration for youtube_summary_v1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from summary.views import index,_login,Home_page,_logout,get_transcription,about,register,history
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', _login, name='login'),
    path('home', Home_page, name='home'),
    path('logout', _logout, name='logout'),
    path('get_summary',get_transcription,name='get_summary'),
    path('about',about,name='about'),
    path('register',register,name='register'),
    path('history',history,name='history'),
    path('', index,name='index'),
]+ static(settings.STATIC_URL, serve,document_root=settings.STATIC_ROOT)
