from django.urls import path
from . import views
urlpatterns = [
    path("",views.Home,name="Home"),
    path('home',views.welcome,name="home"),
    path('query_builder',views.query_builder,name="query_builder"),
    path('users',views.users,name="users"),
]