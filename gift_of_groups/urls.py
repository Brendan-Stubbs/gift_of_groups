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
from uac import views as uac_views
from django.views.generic.base import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", uac_views.Register.as_view(), name="register"),
    path("", include("django.contrib.auth.urls")),
    path("", include("gifts.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("robots.txt", TemplateView.as_view(template_name="gifts/robots.txt", content_type="text/plain"),),
    path("sitemap.xml", TemplateView.as_view(template_name="gifts/sitemaps.xml", content_type="text/xml"),),

]
