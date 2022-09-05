from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm, ItemForm, ItemUpdateForm
from .models import UserProfile, Item

from .models import UserProfile
from .models import Item



# Create your views here.

####### PROFILE VIEWS ##########################################################
@login_required(login_url='/login/')
def profile_create_view(request):
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
        user_items = Item.objects.order_by("-created").filter(user=profile_obj.user)
        context = {
            'profile_obj': profile_obj,
            'user_items': user_items,
        }
    except ObjectDoesNotExist:
        return redirect("/thrift/profile-create/")
    return render(request, "thrift/profile-detail.html", context)

@login_required(login_url='/login/')
def profile_update_view(request, slug):
    profile_obj = get_object_or_404(UserProfile, slug=slug, user=request.user)
    form = UserProfileForm(request.POST or None, instance=profile_obj)
    context = {
        "form": form,
        "profile_obj": profile_obj,
    }
    if form.is_valid():
        form.save()
        context["msg"] = "form was saved"
        return redirect(profile_obj.get_absolute_url())
    return render(request, "thrift/profile-update.html", context)

# def profile_update_view(request, slug):
#     pass
    

####### ITEM VIEWS #############################################################

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
@login_required(login_url='/login/')
def item_detail_view(request, slug):
    """
    1. get the item from the database using the slug
    2. add it to the context to be passed to the template
    """
    item_obj = Item.objects.get(slug=slug)
    context = {
        "item": item_obj
    }
    return render(request, "thrift/item-detail.html", context)

@login_required(login_url='/login/')
def item_update_view(request, slug):
    """
    1. get the item object from the database using the slug
    2. instatiate the form, either blank or filled
    3. add the form and item object to the context
    4. if the form is valid:
        4a. save the form
        4b. add a message to the form
        4c. RETURN a redirect to the item objects detail page
    5. return a render of the item update template
    """
    item_obj = get_object_or_404(Item, slug=slug, user=request.user)
    form = ItemUpdateForm(request.POST or None, instance=item_obj)
    context = {
        "form": form,
        "object": item_obj,
    }
    if form.is_valid():
        form.save()
        context["message"] = "Data saved."
        return redirect(item_obj.get_absolute_url())
    return render(request, "thrift/item-update.html", context)

    
    