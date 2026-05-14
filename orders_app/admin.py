from django.contrib import admin

from orders_app.models import Order


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'offer_type',
        'customer_user',
        'business_user',
        'status',
        'updated_at'
    ]

    list_display_links = ['title']

admin.site.register(Order, OrderAdmin)