from django.db import models
# import django_tables2 as tables

from django.contrib.auth.models import User
# from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choices import CAR_TYPE, DEPOTS, COST_OPT
from .manager import *


def uploaded_location(instance, filename):
    return ("%s/%s") % (instance.make, filename)


# CAR_TYPE = (
#     ('small car', 'SMALL CAR'),
#     ('full-size_car', 'FULL-SIZE CAR'),
#     ('truck', 'TRUCK'),
#     ('luxury', 'LUXURY')
# )


class Order(models.Model):
    Drivers_name = models.CharField(max_length=100, unique=True)
    license_number = models.CharField(max_length=100)
    cell_no = models.CharField(max_length=15)
    address = models.TextField()
    date = models.DateTimeField()
    to = models.DateTimeField()

    def __str__(self):
        return self.Drivers_name

    def     get_absolute_url(self):
        return "/car/detail/%s/" % (self.id)


class PrivateMsg(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()


# shreyus
class Location(models.Model):
    loc_zip = models.CharField(max_length=5)
    loc_name = models.CharField(max_length=20, choices = DEPOTS)
    address = models.TextField()
    vehicle_cap = models.IntegerField(default=0)

    objects = LocationManager()

    def __str__(self):
        return self.loc_name

    def get_absolute_url(self):
        return "/location/%s/" % (self.id)


class Car(models.Model):
    image = models.ImageField(upload_to=uploaded_location, null=True, blank=True)
    make = models.CharField(max_length=100)
    car_type = models.CharField(max_length=50, choices=CAR_TYPE)
    year = models.CharField(max_length=4)
    reg_tag = models.CharField(max_length=10)
    cur_milage = models.IntegerField()
    last_serv = models.IntegerField()
    cost_opt = models.CharField(max_length=50, choices=COST_OPT)
    cost = models.IntegerField(default=0)
    depot = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='vehicle')
    zipcode = models.CharField(max_length=5)
    late_fee = models.IntegerField(default=0)
    booking_status = models.CharField(max_length=50, default='available')
    subscription_charge = models.IntegerField(default=200)

    class vehicle(models.TextChoices):
        Good = 'Good'
        Need_cleaning = 'Need Cleaning'
        Need_maintenance = 'Needs Maintenance'

    vehicle_cond = models.CharField(max_length=100, choices=vehicle.choices)
    objects = CarManager()

    def __str__(self):
        return self.make

    def get_absolute_url(self):
        return "/car/%s/" % (self.id)


class UserDetails(models.Model):
    first_name = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30)
    mobileno = models.CharField(max_length=10)
    birthdate = models.DateField()
    address = models.CharField(max_length=30)
    license_number = models.CharField(max_length=10)
    license_place = models.CharField(max_length=10)
    payment_type = models.CharField(max_length=10)
    credit_card_number = models.CharField(max_length=19)
    credit_card_name = models.CharField(max_length=30)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    acc = models.IntegerField(default=0)
    sub_start = models.DateTimeField(default=0)
    sub_end = models.DateTimeField(default=0)

#    objects = CustomerManager()

    def __str__(self):
        return self.last_name

#Not being used to be removed
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileno = models.IntegerField()
    birthdate = models.DateField()
    address = models.CharField(max_length=30)
    license_number = models.CharField(max_length=10)
    license_place = models.CharField(max_length=30)
    objects = CustomerManager()

    def __str__(self):
        return str(self.user)



class StartSubscribe(models.Model):
    first_name = models.CharField(max_length=30, unique=True)
    start_date = models.DateField()
    payment_type = models.CharField(max_length=10)
    credit_card_number = models.IntegerField()
    credit_card_name = models.CharField(max_length=30)
    expiry_date = models.DateField()
    cvv = models.IntegerField()
    acc = models.IntegerField()

    def __str__(self):
        return self.credit_card_number


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='vehicle')
    depot = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='depot')

    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=50)
    user_tran = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)

    objects = BookingManager()

    def __str__(self):
        return "{}\n{}\n{}\n{}\n{}".format(self.customer.first_name, self.vehicle.make, self.depot.loc_name,
                                           self.start_time, self.end_time)

#   def get_absolute_url(self):
#      return "/car/detail/%s/" % (self.id)
    def get_absolute_url(self):
        return "/car/detail/%s/" % (self.id)

class Transaction(models.Model):
    user_account = models.IntegerField()
    company_account = models.IntegerField()

    def __str__(self):
        return "{}\n{}\n{}\n{}\n{}".format(self.user_account, self.company_account)

class Comment(models.Model):
    comments = models.TextField(verbose_name='')

    def __str__(self):
        return self.comments

# class Subscription(models.Model):
#
#     subscription_charge = models.IntegerField(default=200)
#     def __str__(self):
#         return self.comments