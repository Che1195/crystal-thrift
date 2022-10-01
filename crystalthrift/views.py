from django.shortcuts import render
from thrift.utils import get_item_types_list

from thrift.models import Item

def home_view(request):
    # list all items in the data base by the time they were created
    items = Item.objects.order_by('-created').all()
    context = {
        "items": items,
        "types": get_item_types_list,
    }
    return render(request, "home.html", context)