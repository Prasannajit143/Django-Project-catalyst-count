from django.urls import path
from . import views
urlpatterns = [
    path("",views.Home,name="Home"),
    path('home',views.welcome,name="home"),
    path('query_builder',views.query_builder,name="query_builder"),
    path('users',views.users,name="users"),
    path('delete/<int:pk>/',views.delete,name="delete"),
    path('add_user/',views.add_user,name="add_user"),
    path('save_user',views.save_user,name="save_user")
]

# fdlkjl