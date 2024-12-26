from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserRole)
admin.site.register(Gender)
admin.site.register(UserProfile)
admin.site.register(Module)
admin.site.register(SideMenu)
######################################################
admin.site.register(Permission)
admin.site.register(SecurityGroup)
admin.site.register(UserGroup)
admin.site.register(PermissionGroup)
admin.site.register(GroupedPermission)
admin.site.register(UserPermission)
admin.site.register(DefaultPermission)
######################################################
admin.site.register(ReceivedDocument)
admin.site.register(FCMUserDeviceNotificationToken)