from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from django.views.generic import TemplateView
from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.db.models import Q
from django.contrib import messages
import time
from rest_framework.decorators import api_view

def Home(request):
    return redirect('/accounts/login')

def welcome(request):
    return render(request, 'file_upload.html')

def query_builder(request):

    industry = csvdata.objects.values_list('industry', flat=True).distinct()
    industry_list = list(industry)

    year_founded = csvdata.objects.values_list('year_founded', flat=True).distinct()
    year_founded_list = list(year_founded)

    City = csvdata.objects.values_list('city', flat=True).distinct()
    City_list = list(City)

    state = csvdata.objects.values_list('state', flat=True).distinct()
    state_list = list(state)

    country = csvdata.objects.values_list('country', flat=True).distinct()
    country_list = list(country)

    context = {
        'Industry' : industry_list,
        'year_founded' : year_founded_list,
        'city' : City_list,
        'state' : state_list,
        'country' : country_list

    }
    return render(request,'query_builder.html',context)

def users(requst):
    users = User.objects.all()
    return render(requst,'user.html',{'users': users})

def delete(requst,pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('/users')

def add_user(request):
    return render(request,'add_user.html')

def save_user(requst):
    username = requst.POST.get('username')
    password = requst.POST.get('password')
    email = requst.POST.get('email')
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    new_user.save()
    return redirect('/users')


class CsvUploader(TemplateView):
    def post(self, request):
        t1 = time.perf_counter()
        csv_file = request.FILES['csv']
        dtype_mapping = {
            'year founded': float,
            'current employee estimate': int,
            'total employee estimate': int,
            'name': str,
            'domain': str,
            'industry': str,
            'size range': str,
            'country': str,
            'linkedin url': str,
            'locality': str  
        }
        df = pd.read_csv(csv_file, encoding='utf-8', dtype=dtype_mapping)
        # df[['city', 'state']] = df['locality'].str.extract(r'^(.*?),\s*(.*?)$')
        locality_split = df['locality'].str.split(',', expand=True)
        df['city'] = locality_split[0]
        df['state'] = locality_split[1]
        
        df.drop('locality', axis=1, inplace=True)
        default_int_value = 0
        default_str_value = "None"

        default_values = {
            'year founded': default_int_value,
            'current employee estimate': default_int_value,
            'total employee estimate': default_int_value,
            'name': default_str_value,
            'domain': default_str_value,
            'industry': default_str_value,
            'size range': default_str_value,
            'country': default_str_value,
            'linkedin url': default_str_value,
            'city': default_str_value,
            'state': default_str_value
        }
        df.fillna(default_values, inplace=True)
        print(df.isnull().sum())
        length = len(df)
        var1= length//10
        li = []
        for i in range(0,length,var1):
            li.append(df.iloc[i:var1+i,:])

        if var1*10!=length:
            li.append(df.iloc[var1*10:,:])


        for i in li:
            cursor = connection.cursor()
            cols = 'data_id, name, domain, year_founded, industry, size_range,country,linkdin_url, current_employee_estimate, total_employee_estimate,city,state'
            placeholders = ', '.join(['%s'] * len(i.columns))
            query = f"INSERT INTO app_csvdata ({cols}) VALUES ({placeholders})"
            values = [tuple(row) for row in i.to_numpy()]
            cursor.executemany(query, values)
            connection.commit()
            print("Data inserted successfully!")

        t2 = time.perf_counter()
        print(t2-t1)
        val ="{:.2f}".format(t2-t1)
        messages.success(request,f'File loaded in {val} second ')
        return redirect("/home")

@api_view(['GET'])
def filter(request):
    keyword = request.GET.get('keyword')
    industry = request.GET.get('industry')
    year_founded = request.GET.get('year_founded')
    city = request.GET.get('city')
    state = request.GET.get('state')
    country = request.GET.get('country')

    query = Q()

    if keyword:
        query &= Q(name__icontains=keyword) 
    if industry:
        query &= Q(industry__icontains=industry)
    if year_founded:
        query &= Q(year_founded=year_founded)
    if city:
        query &= Q(city__icontains=city)
    if state:
        query &= Q(state__icontains=state)
    if country:
        query &= Q(country__icontains=country)

    companies = csvdata.objects.filter(query)

    result_count = companies.count()
    messages.success(request,f'{result_count} Records found for the query')
    return redirect('/query_builder')
