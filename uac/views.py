from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm
from django.contrib.auth import authenticate, login


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
            new_user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
        else:
            form = RegisterForm()
            context = {"form": form}
            return render(request, "register/register.html", context)
        return redirect("index")