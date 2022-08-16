from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserProfileForm

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

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    return render(request, "accounts/logout.html", {})

def create_user_profile_view(request):
    form = UserProfileForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        user_profile_object = form.save()
        context["form"] = UserProfileForm()
        return redirect("/")
    return render(request, "accounts/create-user-profile.html", context)
    

