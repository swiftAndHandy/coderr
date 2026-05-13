from django.contrib import admin

from offers_app.models import Offer


# Register your models here.
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'user', 'has_image', 'created_at', 'updated_at']

    def has_image(self, obj):
        return  bool(obj.image)

    has_image.boolean = True


admin.site.register(Offer, OfferAdmin)