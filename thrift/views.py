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
    context = {}
    profile_exists = UserProfile.objects.filter(user=request.user).exists()
    if profile_exists:
        context = {"msg": "You already have a profile"}
    else:
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    profile_object = form.save()
                    profile_object.user = request.user
                    profile_object.save()
                    return redirect("/")
                except IntegrityError as e:
                    return redirect("/")
    context["form"] = UserProfileForm()
    return render(request, "thrift/create-profile.html", context)

@login_required(login_url='/login/')
def detail_profile_view(request):
    try:
        profile_obj = request.user.userprofile
        context = {
            'profile_obj': profile_obj
        }
    except ObjectDoesNotExist:
        return redirect("/thrift/create-profile/")
    return render(request, "thrift/detail-profile.html", context)