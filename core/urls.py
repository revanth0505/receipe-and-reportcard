"""
URL configuration for core project.

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
from home.views import *
from vege.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('' ,home,name="name"),
    path('contact/' ,contact,name="contact"),
    path('about/' ,about,name="about"),
    path('receipes/' ,receipes,name="reciepes"),
    path('delete-receipe/<id>/',delete_receipe,name="delete_receipe"),
    path('update-receipe/<id>/',update_receipe,name="update_receipe"),
    path('login/' ,login_page,name="login"),
    path('logout/' ,logout_page,name="logout"),
    path('register/' ,register_page,name="register"),
    path('admin-details/' ,admin_details,name="admin"),
    path('admin-login/' ,admin_login,name="admin_login"),
    path('admin-register/' ,admin_register,name="admin_register"),
    path('delete-user/<id>/',delete_user,name="delete_user"),
    path('update-user/<id>/',update_user,name="update_user"),
    path('students/',get_students,name="get_students"),
    path('see-marks/<student_id>/',see_marks,name="see_marks"),
    path('send-email/',send_email,name="send_email"),
    path('success-page/' ,success_page,name="success"),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()
