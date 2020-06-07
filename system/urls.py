from django.conf.urls import url
from django.contrib import admin
from system import views
from . import views
from system.booking import *
from .search import *
from accounts.views import login_view
from system import search

urlpatterns = [

    url(r'^$', login_view, name="login"),
    url(r'^carlist/$', views.car_list, name="car_list"),

    #url(r'^carlist/$', system.views.car_list, name = "car_list"),
    #url(r'^createOrder/$', views.order_created, name = "order_create"),
    #url(r'^createOrder/$', create_booking2, name = "order_create"),

    url(r'^(?P<id>\d+)/edit/$', views.car_update, name = "car_edit"),


    url(r'^(?P<id>\d+)/$', views.car_detail, name = "car_detail"),

    #url(r'^detail/(?P<id>\d+)/$', views.order_detail, name = "order_detail"),
    #Shreyus
    url(r'^detail/(?P<id>\d+)/$', booking_detail, name = "booking_detail"),

    url(r'^(?P<id>\d+)/delete/$', views.car_delete, name = "car_delete"),
    #url(r'^(?P<id>\d+)/deleteOrder/$', views.order_delete, name = "order_delete"),
    #shreyus
    url(r'^(?P<id>\d+)/deleteOrder/$', delete_booking, name = "delete_booking"),
    #url(r'^subextend/$', cust_booking, name = "contact"),
    url(r'^modify/$', extend_subscription, name = "extend_subscription"),
    #shreyus
    url(r'^booking/$', cust_booking, name = "contact"),
    url(r'^(?P<id>\d+)/returnveh/$', return_vehicle, name = "return_vehicle"),
    url(r'^newcar/$', views.newcar, name = "newcar"),
    url(r'^car/usersearch/$', user_car_search, name = "usersearch"),
    #shreyus
    url(r'^car/acar/$', available_cars, name = "available_cars"),
    #url(r'^(?P<customer_id>[0-9]+)/createOrder/$', create_booking2, name = "order_create"),
    url(r'^(?P<id>\d+)/createOrder/$', create_booking2, name = "order_create"),
    url(r'^(?P<id>\d+)/like/$', views.like_update, name = "like"),
    url(r'^popularcar/$', views.popular_car, name = "popularcar"),
    url(r'^location/', views.location_list, name = "location_list"),
    url(r'^addLocation/$', views.location, name = "location"),
    url(r'^(?P<id>\d+)/location/$', views.loc_detail, name = "loc_detail"),
    url(r'^(?P<id>\d+)/editloc/$', views.loc_edit, name = "loc_edit"),
    url(r'^(?P<id>\d+)/deleteloc/$', views.loc_delete, name = "loc_delete"),

]
