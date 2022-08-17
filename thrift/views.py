from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import UserProfileForm, ItemForm
from .models import UserProfile

from .models import UserProfile


# Create your views here.
@login_required(login_url='/login/')
def profile_create_view(request):
    print(request.user.id)
    context = {}
    profile_exists = UserProfile.objects.filter(user=request.user).exists()
    if profile_exists:
        context = {"msg": "You already have a profile"}
    else:
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    profile_obj = form.save()
                    profile_obj.user = request.user
                    profile_obj.save()
                    return redirect("/")
                except IntegrityError as e:
                    return redirect("/")
    context["form"] = UserProfileForm()
    return render(request, "thrift/profile-create.html", context)

@login_required(login_url='/login/')
def profile_detail_view(request, slug):
    profile_obj = None
    try:
        profile_obj = UserProfile.objects.get(slug=slug)
        context = {
            'profile_obj': profile_obj
        }
    except ObjectDoesNotExist:
        return redirect("/thrift/profile-create/")
    return render(request, "thrift/profile-detail.html", context)

@login_required(login_url='/login/')
def item_create_view(request):
    context = {}
    profile_exists = UserProfile.objects.filter(user=request.user).exists()
    if profile_exists:
        if request.method == "POST":
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    item_obj = form.save()
                    item_obj.user = request.user
                    item_obj.save()
                    return redirect("/") # should take user to item detail page
                except IntegrityError as e:
                    return redirect("/")
    else:
        context["msg"] = "You must create a profile first"
    context["form"] = ItemForm()
    return render(request, "thrift/item-create.html", context)

# need to implement slug fields for this to make sense
def detail_item_view(request):
    context = {}
    return render(request, "thrift/item-detail.html", context)
    
    