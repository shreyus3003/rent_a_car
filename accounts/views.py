from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
#from .forms import SignUpForm
from system.models import UserDetails
from django.contrib.auth.decorators import login_required


from django.contrib.auth import (
    authenticate,
    login,
    logout,
    models,
)
from .forms import UserLoginForm, UserRegisterForm

#User = get_user_model()

def login_view(request):
    logout(request)
    form1 = UserLoginForm(request.POST or None)

    if form1.is_valid():
        username = form1.cleaned_data.get("username")
        password = form1.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        user1 = User.objects.get(username=username)
        if not request.user.is_staff:
            if user1.is_staff:
                login(request, user)

                return redirect("/admincarlist/")
            login(request, user)
            a = UserDetails.objects.filter(first_name=request.user)
            if not a:
                return redirect("/customercreated/")
            return redirect("/car/usersearch/")
    return render(request, "form.html", {"form": form1, "title": "Login"})

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
#        username = form.cleaned_data['username']
#        password = form.cleaned_data['password']
#        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect("/customercreated/")
    context = {
        "title" : "Registration",
        "form": form,
    }
    return render(request, "form.html", context)

def logout_view(request):
    logout(request)
    form1 = UserLoginForm(request.POST or None)
    return render(request, "form.html", {"form": form1, "title": "Login"})


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()

            return redirect("/login/")
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'form.html', context)





















