from django.contrib import admin

from profile_app.models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'first_name', 'last_name', 'avatar_set']

    def avatar_set(self, obj):
        return bool(obj.file)
    avatar_set.boolean = True

admin.site.register(Profile, ProfileAdmin)