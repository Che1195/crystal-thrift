from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UserProfileForm, ItemForm, ItemImageForm, ItemUpdateForm
from .models import UserProfile, Item, ItemImage

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
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)
    context = {
        "form": form,
        "profile_obj": profile_obj,
    }
    if form.is_valid():
        form.save()
        context["msg"] = "form was saved"
        return redirect(profile_obj.get_absolute_url())
    return render(request, "thrift/profile-update.html", context)

@login_required(login_url='/login/')
def profile_delete_view(request, slug):
    profile_obj = get_object_or_404(UserProfile, slug=slug, user=request.user)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)
    context = {
        "form": form,
        "profile_obj": profile_obj,
    }
    if form.is_valid():
        form.save()
        context["msg"] = "form was saved"
        return redirect(profile_obj.get_absolute_url())
    return render(request, "thrift/profile-delete.html", context)

####### ITEM CRUD VIEWS #############################################################

@login_required(login_url='/login/')
def item_create_view(request):
    context = {}
    profile_exists = UserProfile.objects.filter(user=request.user).exists()
    if profile_exists:
        if request.method == "POST":
            form = ItemForm(request.POST)
            files = request.FILES.getlist("image") # retrieves the files uploaded be the user
            if form.is_valid():
                try:
                    item_obj = form.save(commit=False)
                    item_obj.user = request.user
                    item_obj.save()
                    for image in files:
                        # ADD image validation
                        # ADD error handling
                        ItemImage.objects.create(item = item_obj, image=image)

                    return redirect("/") # should take user to item detail page
                except IntegrityError as e:
                    return redirect("/")
    else:
        context["msg"] = "You must create a profile first"
    context["form"] = ItemForm()
    context["imageform"] = ItemImageForm()
    return render(request, "thrift/item-create.html", context)

# need to implement slug fields for this to make sense
@login_required(login_url='/login/')
def item_detail_view(request, slug):
    item_obj = Item.objects.get(slug=slug)
    item_images = ItemImage.objects.filter(item__slug=slug) # a query of all item images related to this item
    context = {
        "item": item_obj,
        "images": item_images
    }
    return render(request, "thrift/item-detail.html", context)

@login_required(login_url='/login/')
def item_update_view(request, slug):
    item_obj = get_object_or_404(Item, slug=slug, user=request.user)
    item_form = ItemUpdateForm(request.POST or None, request.FILES or None, instance=item_obj)
    context = {
        "item_form": item_form,
        "item": item_obj,
    }
    if item_form.is_valid():
        item_form = item_form.save(commit=False)
        item_form.save()
        context["msg"] = "Data saved."
        success_url = reverse("item-detail", kwargs={"slug": item_obj.slug})
        return redirect(success_url)
    return render(request, "thrift/item-update.html", context)

@login_required(login_url='/login/')
def item_delete_view(request, slug):
    item_obj = get_object_or_404(Item, slug=slug, user=request.user)
    user_profile = get_object_or_404(UserProfile, user=request.user) 
        # needed for redirecting back to user profile after deleting item

    if request.method == "POST": # must be a POST method for verification purposes
        item_obj.delete()
        success_url = reverse("profile-detail", kwargs={"slug": user_profile.slug})
        return redirect(success_url)
    context = {
        "item": item_obj,
    }
    return render(request, "thrift/item-delete.html", context)

# @login_required(login_url='/login/')
# def item_update_hx_view(request, slug):
#     """
#     1. get the item object from the database using the slug
#     2. instatiate the form, either blank or filled
#     3. add the form and item object to the context
#     4. if the form is valid:
#         4a. save the form
#         4b. add a message to the form
#         4c. RETURN a redirect to the item objects detail page
#     5. return a render of the item update template
#     """
#     item_obj = get_object_or_404(Item, slug=slug, user=request.user)
#     item_form = ItemUpdateForm(request.POST or None, instance=item_obj)
#     ItemImageFormset = modelformset_factory(ItemImage, form=ItemImageForm, max_num=5, extra=5)
#     qs = item_obj.item_images.all()
#     item_image_formset = ItemImageFormset(request.POST or None, request.FILES or None, queryset=qs)
#     context = {
#         "item_form": item_form,
#         "item_obj": item_obj,
#         "item_image_formset": item_image_formset,
#     }
#     if all([item_form.is_valid(), item_image_formset.is_valid()]):
#         parent = item_form.save(commit=False)
#         parent.save()
#         for form in item_image_formset:
#             if form.cleaned_data != {}: # stops django from saving empty image forms
#                 child = form.save(commit=False)
#                 if child.item is None:
#                     print("Added new")
#                     child.item = parent
#                     child.save()
#         context["msg"] = "Data saved."
#     if request.htmx:
#         return render(request, "thrift/partials/item-update-form.html", context)
#     return render(request, "thrift/item-update.html", context)


# def item_update_hx_view(request, slug=None):
#     item_obj = get_object_or_404(Item, slug=slug, user=request.user)
#     item_form = RecipeForm(request.POST or None, instance=obj)
#     ItemImageFormset = modelformset_factory(ItemImage, form=ItemImageForm, max_num=5, extra=5)
#     qs = item_obj.item_images.all()
#     item_image_formset = ItemImageFormset(request.POST or None, request.FILES or None, queryset=qs)
#     context = {
#         "item_form": form,
#         "item_image_formset": item_image_formset,
#         "object": item_obj, 
#     }
#     if all([item_form.is_valid(), item_image_formset.is_valid()]):
#         parent = item_form.save(commit=False)
#         parent.save()
#         for form in item_image_formset:
#             if form.cleaned_data != {}: # stops django from saving empty image forms
#                 child = form.save(commit=False)
#                 if child.item is None:
#                     print("Added new")
#                     child.item = parent
#                     child.save()
#         context["message"] = "Data saved."    
    
    