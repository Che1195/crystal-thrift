from django.shortcuts import render

from thrift.models import Item

def home_view(request):
    # list all items in the data base by the time they were created
    items = Item.objects.order_by('-created').all()
    context = {"items": items}
    return render(request, "home.html", context)