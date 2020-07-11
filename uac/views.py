from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm


# Create your views here.
class Register(generic.View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {"form": form}
        return render(request, "register/register.html", context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["email"]
            user.save()
        else:
            form = RegisterForm()
            context = {"form": form}
            return render(request, "register/register.html", context)
        return redirect("index")
