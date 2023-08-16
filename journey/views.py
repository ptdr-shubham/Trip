from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse,FileResponse
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
import pandas as pd
import numpy as np
from openpyxl import Workbook
import os
from django.conf import settings

def createExel(request , queryset):
    l = []
    x = 0
    for i in queryset:
        x += i.trip_distance*i.trip_charge
        s = [i.trip_from,i.trip_to,i.trip_distance,i.trip_intermediate_stops,i.trip_description,i.trip_charge,i.trip_distance*i.trip_charge]
        l.append(s)
    x = "₹"+str(x)
    l.append(["","","","","","",""])
    l.append(["","","","","","",""])
    l.append(["Applicant = " + request.user.first_name +" " + request.user.last_name,"","","","",""])
    l.append(["Toatal Amount =                    ","","","","","",x])
    df = pd.DataFrame(l , columns=["Trip From","Trip To","Distance","Intermediate stops","Description","Charge/K.M.","Amount"])
    df.index = np.arange(1, len(df) + 1)
    df.index.rename('Sr. No.', inplace=True)
    df.to_excel('journey/static/reportFile/Trip_Report.xlsx')

def getStats(queryset):
    totalDistance = 0
    tripCount = 0
    longestTrip = 0
    shortestTrip = 1000000000000
    for trip in queryset:
        totalDistance += trip.trip_distance
        tripCount += 1
        shortestTrip = min(shortestTrip,trip.trip_distance)
        longestTrip = max(longestTrip,trip.trip_distance)
    if(tripCount == 0):
        shortestTrip = 0
    stats = {
        "totalDistance" : totalDistance,
        "tripCount" : tripCount,
        "shortestTrip" : shortestTrip,
        "longestTrip" : longestTrip
    }
    return stats

# Create your views here.
@login_required(login_url= "/login/")
def trip_details(request):
    queryset = Trip.objects.filter(trip_user = request.user)
    createExel(request , queryset)
    context = {'trips':queryset}
    return render(request , "tripdetails.html",context)

@login_required(login_url= "/login/")
def delete_trip(request , id):
    queryset = Trip.objects.get(id = id)
    queryset.delete()
    return redirect('home')

@login_required(login_url= "/login/")
def update_trip(request , id):
    #get correspond object to update
    queryset = Trip.objects.get(id = id)
    #get and update form data
    if(request.method == "POST" ):
            data = request.POST
            trip_user = data.get("trip_user")
            trip_from = data.get("trip_from")
            trip_to = data.get("trip_to")
            trip_distance = data.get("trip_distance")
            trip_charge = data.get("trip_cahrge")
            trip_intermediate_stops = data.get("trip_intermediate_stops")
            trip_description = data.get("trip_description")
        
            #update with new values
            queryset.trip_user = trip_user
            queryset.trip_from = trip_from
            queryset.trip_to = trip_to
            queryset.trip_distance = trip_distance
            queryset.trip_charge = trip_charge
            queryset.trip_intermediate_stops = trip_intermediate_stops
            queryset.trip_description = trip_description
            queryset.save()
            return redirect('home')
    context = {'trip':queryset}
    return render(request , "updateDetails.html" , context)

@login_required(login_url= "/login/")
def leave_update(request):
     return redirect('home')

def login_page(request):
     if(request.method == "POST"):
        #get data from form
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        #handling default unique constraint on username
        user = User.objects.filter(username = username)
        if(user.exists()):
            user = authenticate(username = username , password = password)
            if(user is None):
                messages.info(request , "Invalid Password")
                return redirect("/login/")
            else:
                login(request , user)
                return redirect("/profile/")
        else:
             messages.info(request , "User not found")
             return redirect("/login/")

     return render(request , "login.html")

def register_page(request):
    if(request.method == "POST"):
        #get data from form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        #handling default unique constraint on username
        user = User.objects.filter(username = username)
        if(user.exists()):
            # messages.add_message(request, messages.INFO, "Username Already taken")
            messages.info(request , "Username Already taken")
            return redirect("/register/")

        #create user
        user = User.objects.create(
             first_name = first_name,
             last_name = last_name,
             username = username,
        )
        #set encrypted password
        user.set_password(password)
        user.save()
        # messages.add_message(request, messages.SUCCESS, "Account created Successfully")
        messages.info(request , "Account created Successfully")
        return redirect("/register/")
    return render(request , "register.html")

@login_required(login_url= "/login/")
def profile_page(request):
    if(request.method == "POST"):
        data = request.POST
        trip_user = data.get("trip_user")
        trip_from = data.get("trip_from")
        trip_to = data.get("trip_to")
        trip_distance = data.get("trip_distance")
        trip_charge = data.get("trip_charge")
        trip_intermediate_stops = data.get("trip_intermediate_stops")
        trip_description = data.get("trip_description")
        Trip.objects.create(
            trip_user = trip_user,
            trip_from  = trip_from ,
            trip_to = trip_to ,
            trip_distance = trip_distance ,
            trip_charge = trip_charge ,
            trip_intermediate_stops = trip_intermediate_stops ,
            trip_description = trip_description
        )
        return redirect('/profile/')
    queryset = User.objects.filter(username = request.user.username)
    trips = Trip.objects.filter(trip_user = request.user.username)
    stats = getStats(trips)
    context = {'users':queryset,
               "stats" : stats,
               }
    return render(request , "profile.html",context)

@login_required(login_url= "/login/")
def logout_page(request):
    logout(request)
    return redirect("/login/")


def download(request):
    file = os.path.join(settings.BASE_DIR , 'journey/static/reportFile/Trip_Report.xlsx')
    fileOpened = open(file , 'rb')
    return FileResponse(fileOpened)