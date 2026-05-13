from django.contrib import admin

from offers_app.models import Offer, OfferDetail


# Register your models here.
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'user', 'has_image', 'created_at', 'updated_at']

    def has_image(self, obj):
        return  bool(obj.image)

    has_image.boolean = True

class OfferDetailAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'offer',
        'price',
        'delivery_time_in_days',
        'offer_type',
    ]


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)