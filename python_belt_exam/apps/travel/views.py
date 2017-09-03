from __future__ import unicode_literals
import re
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date, datetime

# Create your views here.
#-----------------------------------------------------------------------------------------------------------

def index(request):
    return render(request, 'travel/index.html')

#-----------------------------------------------------------------------------------------------------------    

#-----------------------------------------------------------------------------------------------------------

def register(request):
    
    full_name = request.POST['full_name']
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    valid = True
    if len(full_name) < 3:
        messages.error(request, '*Name must be at least 3 characters')
        valid = False

    if len(username) < 3:
        messages.error(request, '*Username must be at least 3 characters')
        valid = False
    
    if len(password)< 8:
        messages.error(request, '*Password too short, must be at least 8 characters long.')
        valid = False

    if password != confirm_password:
        messages.error(request, '*Passwords do not match.')
        valid = False

    if valid:
        try: 
            User.objects.create(full_name = full_name, username = username, password = password)
            messages.success(request, '*You have successfully registered. Please sign in.')
            return redirect('/')
        except:
            messages.error(request, '*User exists')
            return redirect('/')
    else:
        return redirect('/')


#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def login(request):
    valid = True
    username = request.POST['username']
    password = request.POST['password']
    user_id = ''
    try:
        user_id = User.objects.get(username=username)
    
    except:
        messages.error(request, '*Invalid User')
        return redirect('/')
    
    if password == user_id.password:
        # print "first name is: ", user_id.first_name
        # print "email is: ", user_email
        request.session['full_name'] = user_id.full_name
        request.session['username'] = username
        request.session['user_id'] = user_id.id
        return redirect('/home')
    else:
        messages.error(request, '*Invalid Password')
        return redirect('/')


#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def home_page(request):
    
    data = Trip.objects.all()
    trips ={
        "trips": data,
        'joined_trips': Trip.objects.filter(travelers__id=request.session['user_id'])
    }
    return render(request, 'travel/home.html', trips)
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def plan(request):
    return render(request, 'travel/plan.html')
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def add(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":

        completed_form = True

        destination = request.POST['destination']
        if len(destination) < 1:
            completed_form = False
            messages.error(request, "Destination is required")


        description = request.POST['description']
        if len(description) < 1:
            completed_form = False
            message.error(request, "Description field can not be empty")

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if start_date < date.today():
                completed_form = False
                messages.error(request,'START Date can not be a past one')
        else:
            messages.error(request,'Must have a valid START date.')

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date < date.today():
                completed_form = False
                messages.error(request,'END Date can not be a past one')
        else:
            messages.error(request,'Must have a valid END date.')

        if start_date and end_date:
            if start_date > end_date:
                completed_form = False
                messages.error(request,'The END date of TRIP can not be before START date.')


        if completed_form:
            user = User.objects.get(pk=request.session['user_id'])

            Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planner=User.objects.get(id=request.session['user_id']))


        else:
            messages.error(request, "please try again")
            return redirect('/plan_form')

    return redirect('/home')
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def view_trip(request, trip_id):
    
    trip = Trip.objects.get(id=trip_id)
    travelers = trip.travelers.all()

    data = {
        'trip': trip,
        'travelers': travelers
    }
    
    return render(request, 'travel/view_trip.html', data)
    
#-----------------------------------------------------------------------------------------------------------
def join(request, trip_id):
    
    tripInQuestion = Trip.objects.get(id=trip_id)
    userThatWantsToJoin = User.objects.get(id=request.session['user_id'])
    tripInQuestion.travelers.add(userThatWantsToJoin)
    tripInQuestion.save()

    return redirect('/home')
#-----------------------------------------------------------------------------------------------------------
def logout(request):
    request.session.clear()
    return redirect('/')
#-----------------------------------------------------------------------------------------------------------
    