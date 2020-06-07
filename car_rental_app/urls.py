"""car_rental_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from system.views import admin_car_list, admin_msg, order_list, \
#     car_created, order_update, order_delete, msg_delete, location_list, \
#     location, loc_detail,customer_created,start_subscription, admin_pge, profile
from system.search import *
from system.views import *
from system.booking import *
from accounts.views import (login_view, register_view, logout_view,register_user)

urlpatterns = [
    url(r'^$', login_view, name="home"),
    url(r'^admin/', admin.site.urls),
    #url(r'^$', admin_car_list, name='adminIndex'),

    url(r'^(?P<id>\d+)/$', car_detail_admin, name = "car_detail_admin"),
    url(r'^listOrder/$', order_list, name = "order_list"),
    #url(r'^(?P<id>\d+)/editOrder/$', order_update, name = "order_edit"),
    #shreyus
    url(r'^(?P<id>\d+)/editOrder/$', update_booking, name = "update_booking"),

    #url(r'^(?P<id>\d+)/deleteOrder/$', order_delete, name = "order_delete"),
    #shreyus
    url(r'^(?P<id>\d+)/deleteOrder/$', delete_booking, name = "delete_booking"),
    url(r'^create/', car_created, name = "car_create"),
    #url(r'^message/$', admin_msg, name='message'),
    #shreyus
    url(r'^message/$', customer_list, name='message'),
    #shreyus
    url(r'^(?P<id>\d+)/deleteCust/$', cust_sub_term, name = "customer_termination"),
    url(r'^(?P<id>\d+)/endsub/$', end_subscription, name = "end_sub"),
    url(r'^(?P<id>\d+)/modprofile/$', modify_profile, name = "modify_profile"),
    url(r'^(?P<id>\d+)/deletemsg/$', msg_delete, name = "msg_delete"),
    url(r'^car/', include('system.urls')),
    url(r'^login/', login_view, name='login'),
    url(r'^car/usersearch/$', user_car_search, name = "usersearch"),
    #shreyus
    url(r'^car/acar/$', available_cars, name = "available_cars"),
    url(r'^car/car_loc_search1/$', car_loc_search1, name = "car_loc_search1"),
    url(r'^logout/', login_view, name='home'),
    url(r'^register/', register_view, name='register'),
    #url(r'^register/', register_user, name='register'),
    url(r'^location/', location_list, name = "location_list"),
    url(r'^addLocation/$', location, name = "location"),
    url(r'^customercreated/$', customer_created, name="customercreated"),
    url(r'^startsubscribe/$', start_subscription, name="startsubscribe"),
    url(r'adminhome/$', admin_pge, name = "adminpge"),
    url(r'^admincarlist/', admin_car_list, name='admin_car_list'),
    url(r'^adminhome/profile/', profile, name="adminpage"),
#    url(r'^cartable/$', CarListView.as_view(), name = "cartable"),
    url(r'details/$', PersonListView, name = "details"),
    url(r'^(?P<id>\d+)/pay/$', pay_booking, name = "pay_booking"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)