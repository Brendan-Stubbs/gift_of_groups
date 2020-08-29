"""gift_of_groups URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from uac import views as uac_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", uac_views.Register.as_view(), name="register"),

    path("reset_password/",
        auth_views.PasswordResetView.as_view(template_name="password_management/password_reset.html"),
        name="reset_password"),

    path("password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password_management/password_reset_sent.html"), 
        name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password_management/password_reset_form.html"), name="password_reset_confirm"),

    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name="password_management/password_reset_complete.html"), 
        name="password_reset_complete"),

    path("", include("django.contrib.auth.urls")),
    path("", include("gifts.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("robots.txt", TemplateView.as_view(template_name="gifts/robots.txt", content_type="text/plain"),),
    path("sitemap.xml", TemplateView.as_view(template_name="gifts/sitemaps.xml", content_type="text/xml"),),

]
