from django.urls import path
from app.views import *
urlpatterns = [
    path("",Home,name="Home"),
    path('home',welcome,name="home"),
    path('query_builder',query_builder,name="query_builder"),
    path('users',users,name="users"),
    path('delete/<int:pk>/',delete,name="delete"),
    path('add_user/',add_user,name="add_user"),
    path('save_user',save_user,name="save_user"),
    path('csv-uploader/', CsvUploader.as_view(), name='csv_uploader'),
]

