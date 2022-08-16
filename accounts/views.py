from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.shortcuts import render, redirect

# Create your views here.
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {'form': form}
    return render(request, "accounts/register.html", context)

def login_view(request):
    if request.method == "POST": # if we are clicking submit on the login button
        form = AuthenticationForm(request, data=request.POST) # fill the form in
        if form.is_valid():
            user = form.get_user() # get the user object
            login(request, user) # log the user in
            return redirect("/") # redirect to the homepage
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, "accounts/login.html", context)

@login_required(login_url='/login/')
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    return render(request, "accounts/logout.html", {})


    

