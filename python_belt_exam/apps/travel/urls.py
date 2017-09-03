from django.conf.urls import url
from . import views

urlpatterns = [   
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home_page),
    url(r'^logout$', views.logout),
    url(r'^add_plan$', views.add),
    url(r'^plan_form$', views.plan),
    url(r'^view_trip/(?P<trip_id>\d+)$', views.view_trip, name='view_trip'),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    

    
    
]
