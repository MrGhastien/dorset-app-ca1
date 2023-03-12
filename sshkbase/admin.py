from django.contrib import admin
from django.contrib.admin import ModelAdmin

from sshkbase.models import User, SSHKey


class UserAdmin(ModelAdmin):
    fieldsets = [
        ('Common attributes', {
            'fields': ('nickname', 'name', 'email')
        }),
        ('Misc', {
             'classes': ('collapse',),
             'fields': ('registerDate',)
         })
    ]


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(SSHKey)
