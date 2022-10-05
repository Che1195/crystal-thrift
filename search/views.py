from django.shortcuts import render
from thrift.utils import get_item_types_list

from thrift.models import Item

def search_view(request):    
    context = {
        "types": get_item_types_list,
    }
    return render(request, "search/search-view.html", context)

def search_results_hx_view(request):
    query = request.GET.get('q') # get query object
    search_type = request.GET.get("type")
    Klass = Item

    qs = Klass.objects.search(query=query).filter(item_type=search_type.capitalize())
    if search_type == "all":
        qs = Klass.objects.search(query=query)

    # if search_type and not query:
    #     qs = Klass.objects.all().filter(item_type=search_type.capitalize())

    context = {
        "queryset": qs,
        "types": get_item_types_list,
    }

    template = "search/results-view.html"
    if request.htmx:
        template = "search/partials/results.html"
    return render(request, template, context)