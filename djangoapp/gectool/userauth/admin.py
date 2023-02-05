from django.contrib import admin
from .models import Profile, PremiumUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class PremiumUserInline(admin.StackedInline):
    model = PremiumUser
    can_delete = False
    verbose_name_plural = 'Premium Users'


class CustomizedUserAdmin (UserAdmin):
    inlines = (ProfileInline, PremiumUserInline)


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

# to show profile sepearately in the admin tab
admin.site.register(Profile)
admin.site.register(PremiumUser)