from django.db import models
#from .booking import sf_time

from django.contrib.auth.models import UserManager

import datetime


class LocationQuerySet(models.QuerySet):
    def depots(self, loc_name=None):
        if loc_name:
            return self.filter(loc_name=loc_name)
        return self


class LocationManager(models.Manager):
    def create_depot(self, loc_name):
        return self.create(loc_name=loc_name)

    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db)

    def depots(self, loc_name=None):
        if loc_name:
            return self.get_queryset().depots(loc_name=loc_name)
        return self.get_queryset().depots()


class CarQuerySet(models.QuerySet):
    def cars(self, depot=None, car_type=None):
        if not depot:
            return self
        elif not car_type:
            return self.filter(depot=depot)
        else:
            return self.filter(depot=depot, car_type=car_type)


class CarManager(models.Manager):
    def create_vehicle(self, depot, car_type):
        return self.create(depot=depot, car_type=car_type)

    def update_status(self, vehicle):
        vehicle.booking_status = 'available'
        vehicle.save()

    def get_queryset(self):
        return CarQuerySet(self.model, using=self._db)

    def cars(self, depot=None, car_type=None):
        if not depot:
            return self.get_queryset().cars()
        elif not car_type:
            return self.get_queryset().cars(depot)
        else:
            return self.get_queryset().cars(depot, car_type)


class CustomerManager(models.Manager):
    def create_customer(self, username, first_name, hours, email, password):
        return self.create(username=username, first_name=first_name, last_name=hours, email=email, password=password)


class BookingQuerySet(models.QuerySet):
    def bookings(self, customer=None, vehicle=None, depot=None):
        if vehicle and depot:
            return self.filter(vehicle=vehicle, depot=depot)
        if customer:
            return self.filter(customer=customer)
        if vehicle:
            return self.filter(vehicle=vehicle)
        if depot:
            return self.filter(depot=depot)
        return self


class BookingManager(models.Manager):
    def create_booking(self, customer, vehicle, depot, start_time, end_time):
        #sf_time()
        if start_time > end_time:
            return 0
        td = end_time - start_time
        days, seconds = td.days, td.seconds
        hours = days * 24 + seconds // 3600
        customer.last_name=4320

        if hours > 72:
            return 1

        cost_opt = vehicle.cost_opt
        cost  = vehicle.cost
        if cost_opt == "PER-HOUR":
            amount = cost * hours
        elif cost_opt == "1-5H":
            h = hours/5
            amount = cost * h
        elif cost_opt == "6-10H":
            h = hours/10
            amount = h * cost
        else:
            h = hours/24
            amount = h * cost

        print(cost_opt)
        print(amount)

        try:
            if hours > int(customer.last_name):
                return -1
        except:
            return -2

        #customer.last_name = "{}".format(int(customer.last_name) - hours)
        #customer.save()
        vehicle.booking_status = 'booked'
        vehicle.save()
        return self.create(customer=customer, vehicle=vehicle, depot=depot, start_time=start_time, end_time=end_time,\
                           hours=hours, user_tran=amount)

    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def bookings(self, customer=None, vehicle=None, depot=None, start_time=None):
        if start_time and customer:
            return self.get_queryset().bookings(customer=customer, start_time=start_time)
        if customer:
            return self.get_queryset().bookings(customer=customer)
        if vehicle:
            return self.get_queryset().bookings(vehicle=vehicle)
        if depot:
            return self.get_queryset().bookings(depot=depot)
        return self.get_queryset().bookings()

    def delete_booking(self, customer, booking):
        start_time = booking.start_time
        end_time = booking.end_time
        td = end_time - start_time
        days, seconds = td.days, td.seconds
        hours = days * 24 + seconds // 3600

        customer.last_name = "{}".format(int(customer.last_name) + hours)
        #customer.save()
        booking.delete()
