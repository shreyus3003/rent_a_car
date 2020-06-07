from django.contrib import admin
from .models import Car, Order, PrivateMsg, Location, UserDetails, StartSubscribe, User, Booking, Comment
# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ("make","car_type","year","late_fee","reg_tag","cost_opt","cost","booking_status","depot","zipcode","vehicle_cond")
class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "to", "Drivers_name")

class PrivateMsgAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")

class LocationAdmin(admin.ModelAdmin):
    list_display = ("loc_name", "loc_zip", "address", "vehicle_cap")

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","license_number","license_place","acc", "sub_start", "sub_end",)

class StartSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("start_date","payment_type", "credit_card_number", "credit_card_name", "expiry_date","cvv", "acc",)

class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer", "vehicle", "depot", "start_time", "end_time","status", "user_tran", "hours",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment",)

admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PrivateMsg, PrivateMsgAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserDetails, CustomerAdmin)
admin.site.register(StartSubscribe,StartSubscriptionAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Comment)