from django.contrib import admin

from .models import *


@admin.register(Account)

class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'username','date_joined']
    list_filter=['username','country']
    readonly_fields = ('date_joined', 'last_login')  
    ordering = ['-date_joined']
    
admin.site.register(UserDevice)    
admin.site.register(Contact)

