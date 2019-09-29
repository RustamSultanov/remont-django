from django.contrib import admin
from .models import Appeal,UserAccept,Rubricator,MessegesAppeal,Company,Order,Adress,Guaranty,Estimate,Stage,Card,Feedback
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from mptt.admin import MPTTModelAdmin


class UserAcceptInline(admin.StackedInline):
    model = UserAccept
    can_delete = False
    verbose_name_plural = 'Users'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserAcceptInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Order)
admin.site.register(Card)
admin.site.register(Feedback)
admin.site.register(Adress)
admin.site.register(Stage)
admin.site.register(Estimate)
admin.site.register(Guaranty)
admin.site.register(Appeal)
admin.site.register(Company)
admin.site.register(MessegesAppeal)
admin.site.register(Rubricator,MPTTModelAdmin)
