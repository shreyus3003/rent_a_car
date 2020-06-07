from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse , HttpResponseRedirect
from django.db.models import Q
import datetime
from django.utils import timezone
#from .tables import PersonTable
from dateutil.relativedelta import relativedelta

from .models import Car, Order, PrivateMsg, Location ,StartSubscribe, Customer, User, Booking
from .forms import CarForm, OrderForm, MessageForm, LocationForm, UserDetail, StartSubcription
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
#from django_tables2 import SingleTableView
from .models import UserDetails

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    models,
)

from django.contrib.auth.decorators import login_required

User = get_user_model()
#from .tables import PersonTable

sf =  pytz.timezone("America/Los_Angeles")
timezone.activate(sf)

def home(request):
    context = {
        "title" : "Rent a Car"
    }
    return render(request,'home.html', context)

def car_list(request):
    car = Car.objects.all()
    print(car)

    query = request.GET.get('q')
    if query:
        car = car.filter(
                     Q(make__icontains=query) |
                     Q(car_type__icontains = query) |
                     Q(cost_opt__icontains=query) |
                     Q(cost__icontains=query)
                            )

    # pagination
    paginator = Paginator(car, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'car_list.html', context)

def car_detail(request, id=None):
    detail = get_object_or_404(Car,id=id)
    context = {
        "detail": detail
    }
    return render(request, 'car_detail.html', context)

def car_detail_admin(request, id=None):
    detail = get_object_or_404(Car,id=id)
    context = {
        "detail": detail
    }
    return render(request, 'admin/car_detail_admin.html', context)

def car_created(request):
    form = CarForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        #data = form.data.get()
        #print(data)
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/admincarlist")
    context = {
        "form" : form,
        "title": "Create Car"
    }
    return render(request, 'car_create.html', context)

def car_update(request, id=None):
    detail = get_object_or_404(Car, id=id)
    form = CarForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/admincarlist/")
    context = {
        "form": form,
        "title": "Update Car"
    }
    return render(request, 'car_create.html', context)

#shreyus
def location(request):
    form = LocationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/location")
    context = {
        "form": form,
        "title": "Add Location"
    }
    return render(request, 'addLocation.html', context)

def location_list(request):
    loc = Location.objects.order_by('-id')
    #car = Car.objects.order_by('-id')

    query = request.GET.get('q')
    if query:
        car = car.filter(
            Q(loc_name__icontains=query) |
            Q(address__icontains=query) |
            Q(vehicle_cap__icontains=query)
        )

    # pagination
    paginator = Paginator(loc, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        loc = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        loc = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        loc = paginator.page(paginator.num_pages)
    context = {
        'loc': loc,
    }
    print(context)
    return render(request, 'location.html', context)

def loc_edit(request,id=None):
    detail = get_object_or_404(Location, id=id)
    form = LocationForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Edit Location"
    }
    return render(request, 'addLocation.html', context)

def loc_delete(request,id=None):
    query = get_object_or_404(Location,id = id)
    query.delete()
    return HttpResponseRedirect("/location")

def loc_detail(request):
    return render(request, 'admin_index.html', context)


def car_delete(request,id=None):
    query = get_object_or_404(Car,id = id)
    query.delete()

    car = Car.objects.all()
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)
#customer details

def customer_created(request):
    a = UserDetails.objects.filter(first_name=request.user)
    user = get_object_or_404(User, first_name=request.user)

    cuser= get_user_model()
    print("cuser")
    print(cuser.first_name)
    print("user")
    print(user.first_name)

    if not a:
        form = UserDetail(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.save()
            instance.acc = 200
            instance.first_name=user
            instance.last_name = user.last_name
            instance.sub_start = timezone.localtime(timezone.now())
            instance.sub_end = timezone.localtime(timezone.now()) + relativedelta(months=+6)
            instance.save()

            return HttpResponseRedirect("/car/usersearch/")

        context = {
            "form": form,
            "title": "Enter Details and Subscribe",
            "user":user
        }
        return render(request, 'customer_details.html', context)
    return HttpResponseRedirect("/details/")

# Subscription begin

def start_subscription(request):
    form = StartSubcription(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/car/newcar/")

    context = {
        "form": form,
        "title": "start subscription"
    }
    return render(request, 'customer_details.html', context)


#order
#Shreyus
def order_list(request):
    order = Booking.objects.all()

    query = request.GET.get('q')
    if query:
        order = order.filter(
            Q(customer__icontains=query)|
            Q(vehicle__icontains=query)
        )

    # pagination
    paginator = Paginator(order, 4)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        order = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        order = paginator.page(paginator.num_pages)
    context = {
        'order': order,
    }
    print(order)
    return render(request, 'admin/order_list.html', context)

def order_detail(request, id=None):
    detail = get_object_or_404(Order,id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'order_detail.html', context)

def order_created(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": "Create Order"
    }
    return render(request, 'order_create.html', context)

def order_update(request, id=None):
    detail = get_object_or_404(Order, id=id)
    form = OrderForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Order"
    }
    return render(request, 'order_create.html', context)

def order_delete(request,id=None):
    query = get_object_or_404(Order,id = id)
    query.delete()
    return HttpResponseRedirect("/listOrder/")

def newcar(request):
    print("called in newcar")
    new = Car.objects.order_by('-id')
    #seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(make__icontains=query) |
            Q(car_type__icontains=query) |
            Q(vehicle_cond__icontains=query) |
            Q(cost_per_day__icontains=query)
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
    return render(request, 'new_car.html', context)

def like_update(request, id=None):
    new = Car.objects.order_by('-id')
    like_count = get_object_or_404(Car, id=id)
    like_count.like+=1
    like_count.save()
    context = {
        'car': new,
    }
    return render(request,'new_car.html',context)

def popular_car(request):
    new = Car.objects.order_by('-like')
    # seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(make__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_per_day__icontains=query)
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
    return render(request, 'new_car.html', context)



def contact(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/car")
    context = {
        "form": form,
        "title": "Contact With Us",
    }
    return render(request,'contact.html', context)

#-----------------Admin Section-----------------


@login_required
def admin_car_list(request):
    car = Car.objects.order_by('-id')

    query = request.GET.get('q')
    if query:
        car = car.filter(
            Q(make__icontains=query) |
            Q(car_type__icontains=query) |
            Q(cost_opt__icontains=query) |
            Q(cost__icontains=query)
        )

    # pagination
    paginator = Paginator(car, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    print(context)
    return render(request, 'admin_index.html', context)

def admin_msg(request):
    msg = PrivateMsg.objects.order_by('-id')
    context={
        "car": msg,
    }
    return render(request, 'admin_msg.html', context)

def admin_pge(request):
    return render(request, 'admin/admin_home.html')


def msg_delete(request,id=None):
    query = get_object_or_404(PrivateMsg, id=id)
    query.delete()
    return HttpResponseRedirect("/message/")
from django.shortcuts import render

# #
# class PersonListView(SingleTableView):
#     model = UserDetails
#     table_class = PersonTable
#     queryset = UserDetails.objects.all()
#     template_name = 'templates/user_summary.html'
#


# def PersonListView(request):
#     latest_question_list = get_object_or_404(UserDetails.objects.all())
#     if request.method =='POST':
#         form=UserDetail(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/car/newcar/')
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = UserDetail(initial={'renewal_date': proposed_renewal_date})
#
#     template=loader.get_template('user_summary.html')
#     context = {'form':form,
#         'latest_question_list': latest_question_list}
#     return HttpResponse(template.render(context, request))





# def PersonListView(request):
#     AuthorFormSet = UserDetail(UserDetails)
#     if request.method == "POST":
#         formset = AuthorFormSet(
#             request.POST, request.FILES,
#             queryset=UserDetails.objects.filter(first_name__startswith=''),
#         )
#         if formset.is_valid():
#             formset.save()
#             # Do something.
#     else:
#         formset = AuthorFormSet(queryset=UserDetails.objects.filter(first_name__startswith=''))
#     return render(request, 'user_summary.html', {'formset': formset})


# class PersonListView(ListView):
#     model = Post = UserDetails
#     template_name = 'user_summary.html'
#
#     def get_queryset(self):
#         user = get_object_or_404(UserDetails, username=self.kwargs.get('first_name'))
#         return UserDetails.objects.filter(author=user)
#
#     def get_username_field(self):
#         user = get_object_or_404(UserDetails, username=self.kwargs.get('username'))
#         return UserDetails.objects.filter(user=user)

def PersonListView(request):

    print(request.user)
    user_list = UserDetails.objects.filter(first_name=request.user)
    
    print(user_list)
    return render(request, 'User/userprofile.html', {'obj1': user_list})


# def Subscription(request):
#     form = SubcriptionForm(request.POST or None, request.FILES or None)
#
#     if form.is_valid():
#         # data = form.data.get()
#         # print(data)
#         instance = form.save(commit=False)
#         instance.save()
#         return HttpResponseRedirect("/admincarlist")
#     context = {
#         "form": form,
#         "title": "Subscription charge"
#     }
#     return render(request, 'admin/subscription.html', context)

@login_required
def profile(request):
    return render(request, 'admin/profile.html')