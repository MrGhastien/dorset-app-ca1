from django.contrib import admin

from sshkbase.models import User, SSHKey

# Register your models here.

admin.site.register(User)
admin.site.register(SSHKey)
