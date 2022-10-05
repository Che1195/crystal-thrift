"""crystalthrift URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import home_view
from accounts.views import (
    register_view,
    login_view,
    logout_view,
)
from thrift.views import (
    # Profile CRUD Views
    profile_create_view,
    profile_detail_view,
    profile_update_view,
    user_delete_view,
    # Item CRUD Views
    item_create_view,
    item_detail_view,
    item_update_view,
    item_delete_view,
)
from search.views import (
    search_view,
    search_results_hx_view,
)

urlpatterns = [
    # standard views
    path('', home_view, name="home"),
    path('admin/', admin.site.urls),
    # account views
    path('register/', register_view),
    path('login/', login_view, name="login"),
    path('logout/', logout_view),
    # thrift views
    path('thrift/profile-create/', profile_create_view),
    path('thrift/profile-detail/<slug:slug>/', profile_detail_view, name="profile-detail"),
    path('thrift/profile-update/<slug:slug>/', profile_update_view),
    path('thrift/user-delete/<slug:slug>/', user_delete_view),
    path('thrift/item-create/', item_create_view),
    path('thrift/item-detail/<slug:slug>/', item_detail_view, name="item-detail"),
    path('thrift/item-update/<slug:slug>/', item_update_view),
    path('thrift/item-delete/<slug:slug>/', item_delete_view),
    # search views
    path('search-listings/', search_view, name="search-listings"),
    path('search/', search_results_hx_view, name="search"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# connects our projects url patterns to the media url patterns
