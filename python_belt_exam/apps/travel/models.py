# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt, re
from datetime import date, datetime
# Create your models here.

class TripManager(models.Manager):
    def add(self, request):
        
        user = User.objects.get(id=request.session['user']['user_id'])

        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planner=user)
#-----------------------------------------------------------------------------------------------------------

    def join(self, request, id):
        user = User.objects.get(id=request.session['user_id'])

        trip = Trip.objects.get(id=id)

        trip.travelers.add(user)
#-----------------------------------------------------------------------------------------------------------


    def auth(self, request):

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date:
            start_date = datetime.datetime.strptime("%Y-%m-%d").date()
            if start_date < date.today():
                messages.error('Date can not be a past one')
        else:
            messages.error('Must have a valid START date.')

        if end_date:
            end_date = datetime.datetime.strptime("%Y-%m-%d").date()
            if end_date < date.today():
                messages.error('Date can not be a past one')
        else:
            messages.error('Must have a valid END date.')

        if start_date and end_date:
            if start_date > end_date:
                messages.error('The END date of TRIP can not be before START date.')
            
        if not request.POST['destination']:
            messages.error('Destination field can not be empty.')

        if not request.POST['description']:
            messages.error('Description field can not be empty.')
#-----------------------------------------------------------------------------------------------------------


class User(models.Model):
    full_name = models.CharField(max_length=65)
    username = models.CharField(max_length=65)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    planner = models.ForeignKey(User, related_name='trip')
    travelers = models.ManyToManyField(User, related_name='trips')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  