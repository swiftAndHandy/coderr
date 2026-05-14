from django.contrib import admin

from review_app.models import Review


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business_user', 'reviewer', 'rating', 'description', 'updated_at']

admin.site.register(Review, ReviewAdmin)