"""
URL configuration for rule_engine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Login, Index, Logout, UserList, UserDetail, UserCreate, UserDelete, UserActivation

urlpatterns = [
    path('', login_required(Index.as_view(), login_url='login'), name='index'),
    path('admin/', admin.site.urls),

    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('users', UserList.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('users/create', UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/delete', UserDelete.as_view(), name='user_delete'),
    path('users/active/<str:key>', UserActivation.as_view(), name='user_activation'),

]
