from django.shortcuts import render
from django.views import generic


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, "gifts/index.html", {})
