from django.shortcuts import render
from thrift.utils import get_item_types_list

from thrift.models import Item

def home_view(request):
    # list all items in the data base by the time they were created
    items = []
    if request.user.is_authenticated:
        items = Item.objects.exclude(user=request.user).order_by('-created')
    else:
        items = Item.objects.order_by('-created')
    context = {
        "items": items,
        "types": get_item_types_list,
    }
    return render(request, "home.html", context)