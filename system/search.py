from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse , HttpResponseRedirect
from django.db.models import Q

from .models import Car, Order, PrivateMsg, Location, UserDetails,StartSubscribe
#from .forms import CarForm, OrderForm, MessageForm, LocationForm, UserDetail, StartSubcription
from django.contrib.auth.decorators import login_required
#from .tables import PersonTable
from django.views.generic import ListView
#from django_tables2 import SingleTableView
import re
from .models import UserDetails
#from .tables import PersonTable
from django.views.generic import ListView


def car_loc_search1(request):
    query = request.GET['q']
    print(query)
    # wordList = re.compile('([^,\s]+)').findall(query)
    # print(wordList[0])
    inventory = Car.objects.filter(zipcode__icontains=query)
    #print(inventory.depot)
    print(inventory)
    context = {
        'inventory': inventory,
    }
    print(context)
    return render(request, 'User/userlocsearch.html', context)


def car_loc_search(request):
    new = Location.objects.order_by('-id')
    print(new)
    #seach
    query = request.GET.get('q')
    print(query)
    if query:
        new = new.filter(
            Q(loc_id__icontains=query) |
            Q(loc_name__icontains=query) |
            Q(loc_zip__icontains=query) |
            Q(vehicle_cap__icontains=query)
        )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'User/userpage.html', context)


# class CarListView(SingleTableView):
#     model = Car
#     template_name = 'User/car_table.html'



def user_car_search(request):
    a = UserDetails.objects.filter(first_name=request.user)
    print("inside search")
    if not a:
        return redirect("/customercreated/")
    new = Car.objects.order_by('-id')
    #print(new)
    #seach
    query = request.GET.get('q')
    #print(query)
    if query:
        new = new.filter(
            Q(make__icontains=query)

        )

    query_loc = request.GET.get('p')

    if query_loc:
         new = new.filter(
             Q(zipcode__icontains=query_loc)
         )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'User/userpage.html', context)

def available_cars(request):
    new = Car.objects.filter(booking_status='available')
    print(new)
    #seach
    query = request.GET.get('q')
    #print(query)
    if query:
        new = new.filter(
            Q(make__icontains=query) |
            Q(car_type__icontains=query) |
            Q(vehicle_cond__icontains=query) |
            Q(cost__icontains=query)
        )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'User/availablecars.html', context)
