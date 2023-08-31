from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from django.db import connection
import pandas as pd
from django.db.models import Q
from django.contrib import messages
import time

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
    template_name = 'file_upload.html'
    def post(self, request):
        t1 = time.perf_counter()
        csv_file = request.FILES['csv']
        file = pd.read_csv(csv_file,encoding='utf-8') 
        locality_split = file['locality'].str.split(',', expand=True)
        file['city'] = locality_split[0]
        file['state'] = locality_split[1]
        file.drop('locality', axis=1, inplace=True)
        df =file.dropna()
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
        messages.success(request,f'File loaded within {t2-t1} sec ')
        return redirect("/home")
    
def filter(request):
    keyword = request.POST.get('keyword')
    industry = request.POST.get('industry')
    year_founded = request.POST.get('year_founded')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')

    query = csvdata.objects.filter(Q(name__icontains=keyword) or Q(industry=industry) or Q(year_founded=year_founded) or
                                   Q(city=city) or Q(state=state) or Q(country=country) )
    count=query.count()
    print(query.count())
    # messages.add_message(request,  )
    messages.success(request,f'{count} records found for the query')
    return redirect('/query_builder')
