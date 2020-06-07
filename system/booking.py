from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import *
from .forms import *
from .manager import *

sf =  pytz.timezone("America/Los_Angeles")

def sf_time():
    sf =  pytz.timezone("America/Los_Angeles")
    timezone.activate(sf)

def is_user(request, customer_id):
    current_customer = User.objects.get(id=customer_id)
    if not request.user == current_customer:
        return HttpResponse(404)


def create_booking(request):
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

def create_booking1(request, id=None):

    form = CreateBookingForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": "Create Order"
    }
    return render(request, 'order_create.html', context)

def booking_detail(request, id=None):
    detail = get_object_or_404(Booking,id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'User/bookingdetails.html', context)

#def create_booking(request, customer_id):
@login_required
@csrf_exempt
def create_booking2(request, id=None):
    #sf_time()
    query = get_object_or_404(Car,id = id)
    valid = "true"
    #query = Car.objects.get(make=)
    print(query.car_type)
    print("valid original value",valid)
    if request.method == 'POST':
        form = CreateBookingForm(request.POST)
        form.depot = query.depot
        if form.is_valid():
            customer = request.user
            customer.save()

            #depot = form.cleaned_data['depot']
            #vehicle_type = form.cleaned_data['vehicle_type']
            depot = query.depot
            vehicle_type = query.car_type
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']


            now = timezone.localtime(timezone.now())
            print("printing now",now)
            print("printing start time",start_time)
            if start_time<now:
                print("start is less than now")
                valid="false"

            d = Location.objects.depots(depot)

            vehicle = Car.objects.cars(d[0], vehicle_type)
            print(vehicle)
            v = 0
            for item in vehicle:
                print("Item is", item)
                print("car make", query.make)
                bookings = Booking.objects.bookings(depot=d[0], vehicle=item)
                if not bookings:
                    if item == query:
                        print("inside not booking")
                        v = item
                        print(item)
                #break

                for booking in bookings:
                    print(booking)
                    b_start = booking.start_time - datetime.timedelta(days=2)
                    b_end = booking.end_time + datetime.timedelta(days=2)

                    if (start_time > b_end) or (end_time < b_start):
                        v = item
                        break
                if v:
                    break

            #v = item
            if not v:
                print("currently the vehicle is unavailable")
                return HttpResponseRedirect("/car/acar/")

#            print(b)
            #return render(request, 'order_create.html')
            if valid == "true":
                b = Booking.objects.create_booking(customer, v, d[0], start_time, end_time)
                if b == 1 or b == 0:
                    print("Please book for less than 72 hours")
                    valid = "false"
                else:
                    b.save()
                    return HttpResponseRedirect(b.get_absolute_url())
    else:
        form = CreateBookingForm()
    return render(request, 'order_create.html', {"form":form, "query":query,"valid":valid})

def delete_booking(request,id=None):
    c_charges = 0
    query = get_object_or_404(Booking,id = id)
    customer = request.user
    sf_time()
    t_start = query.start_time
    #t_start = t_start - relativedelta(hours=7)
    print("t_start", t_start)
    now = timezone.localtime(timezone.now())

    td = t_start - now
    days, seconds = td.days, td.seconds
    hours = days * 24 + seconds // 3600
    print(hours)

    hours_min = hours*60
    if (hours_min < 60):
        print("deduct the amount")
        c_charges = 0.1*(query.user_tran)

    else:
        print("amount refunded")

    v = query.vehicle
    Car.objects.update_status(v)
    query.delete()
    r_charges = query.user_tran-c_charges
    return render(request, 'User/cancelbooking.html',{'c_charges':c_charges,'r_charges':r_charges})

def return_vehicle(request, id=None):
    query = get_object_or_404(Booking, id=id)
    car_det = get_object_or_404(Car, make=query.vehicle)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.save()
    print(form)
    sf_time()
    t_end = query.end_time
    t_end = t_end - relativedelta(hours=7)
    print(t_end)
    now = timezone.localtime(timezone.now())
    print(now)
    late_charges = 0
    if (now > t_end):
        # td = now - t_end
        # days, seconds = td.days, td.seconds
        # hours = days * 24 + seconds // 3600
        late_charges = car_det.late_fee
        print("late charge of %d amount is deducted from account", late_charges)
    v = query.vehicle
    Car.objects.update_status(v)
    query.delete()
    return render(request, 'User/return_car.html',{'form':form,'late_charges':late_charges})

def update_booking(request, id=None):
    detail = get_object_or_404(Booking, id=id)
    form = CreateBookingForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Order"
    }
    return render(request, 'order_create.html', context)

def customer_list(request):
    c_list = UserDetails.objects.all()
    print(c_list)

    query = request.GET.get('q')
    if query:
        c_list = c_list.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)
        )

    # pagination
    paginator = Paginator(c_list, 4)  # Show 15 contacts per page
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
        'c_list': c_list,
    }
    print(c_list)
    return render(request, 'admin/admin_cust_view.html', context)

def cust_sub_term(request, id=None):
    query = get_object_or_404(UserDetails, id=id)
    query.delete()
    return HttpResponseRedirect("/message/")

# def cust_booking1 (request):
#     detail = get_object_or_404(Booking,customer=request.user)
#     context = {
#         "detail": detail,
#     }
#     return render(request, 'User/bookingdetails.html', context)

def cust_booking (request):
    c_book = Booking.objects.filter(customer=request.user)
    query = request.GET.get('q')
    if query:
        c_book = c_book.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)
        )

    # pagination
    paginator = Paginator(c_book, 4)  # Show 15 contacts per page
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
        'c_book': c_book,
    }
    #print(c_book)
    return render(request, 'User/mybooking.html', context)

def extend_subscription(request, id=None):
    sf_time()
    detail = get_object_or_404(UserDetails, first_name=request.user)
    #detail.sub_start = timezone.localtime(timezone.now())
    temp = detail.sub_end
    detail.sub_end = temp + relativedelta(months=+6)
    detail.acc = detail.acc + 200
    detail.save()
    context = {
        "detail": detail
    }
    return render(request, 'User/extendsub.html', context)

def modify_profile(request, id=None):
    sf_time()
    detail = get_object_or_404(UserDetails, id=id)
    form = UserDetail(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/details/")

    context = {
        "form": form,
        "title": "Modify Profile"
    }
    return render(request, 'User/modifyprofile.html', context)
#return HttpResponseRedirect("/details/")

def end_subscription(request, id=None):
    query = get_object_or_404(UserDetails, id=id)
    query.delete()
    return redirect("/car/usersearch/")


def pay_booking(request, id=None):
    detail = get_object_or_404(Booking, id=id)

    return render(request, 'User/pay_booking.html', {"detail":detail})

def comments(request):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        return redirect("/car/usersearch/")

    return render(request, "User/availablecars.html")