from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import UserProfileForm
from .models import UserProfile

# Create your views here.
@login_required(login_url='/login/')
def create_profile_view(request):
    form = UserProfileForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        try:
            profile_object = form.save()
            profile_object.user = request.user
            profile_object.save()
            context["form"] = UserProfileForm()
            return redirect("/")
        except IntegrityError as e:
            return redirect("/")
    return render(request, "thrift/create-profile.html", context)

@login_required(login_url='/login/')
def detail_profile_view(request):
    try:
        profile_obj = request.user.userprofile
        context = {
            'profile_obj': profile_obj
        }
    except ObjectDoesNotExist:
        return redirect("/create-profile/")
    return render(request, "thrift/detail-profile.html", context)