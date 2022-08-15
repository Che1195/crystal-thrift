from django.shortcuts import render

def home_view(request):
    msg = """
    Che, this is the first website page you have created without using a 
    a tutorial as a guide. CONGRATS BIG BOY
    """
    context = {
        "msg": msg,
    }
    return render(request, "home.html", context)