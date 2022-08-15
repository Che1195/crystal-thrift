from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
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
