from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from datetime import date
# from django.contrib import admin



class UserRole(models.Model):
    role_name = models.CharField(max_length=255)
    initials = models.CharField(max_length=255, null=True, blank=True, unique=True)
    code_name = models.CharField(max_length=255, unique=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.role_name
    
class Gender(models.Model):
    gender_name = models.CharField(max_length=255)
    initials = models.CharField(max_length=255, null=True, blank=True, unique=True)
    code_name = models.CharField(max_length=255, unique=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.gender_name

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    phoneno = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.FileField(
        upload_to="images/photos/",
        default="images/photos/default.png",
        null=True,
        blank=True,
    )
    is_editable = models.BooleanField(default=True)
    is_deletable = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.user


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()


# Main Application Modules
class Module(models.Model):
    en_module_name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    route_name = models.CharField(max_length=255)
    is_a_sub_module = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    main_module_id = models.IntegerField(null=True, blank=True)
    sort_value = models.IntegerField()
    depth = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.en_module_name


# Side Menu Modules
class SideMenu(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sort_value = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    has_been_modified = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __str__(self):
        return "%s" % self.module


# Dashboard menu model
class DashboardMenu(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sort_value = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    has_been_modified = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __str__(self):
        return "%s" % self.module.en_module_name


class Permission(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    en_permission_name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    is_module_permission = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    has_been_modified = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __str__(self):
        return "%s" % self.en_permission_name


# These charges apply to one student in an active session of a certain class


class SecurityGroup(models.Model):
    en_group_name = models.CharField(max_length=500)
    code_name = models.CharField(max_length=300)
    is_disabled = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)
    is_deletable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.en_group_name


# User Group (A security group To Which the User Belongs Tooo)
class UserGroup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    has_been_modified = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __str__(self):
        return "%s - %s" % (self.user, self.security_group)


class PermissionGroup(models.Model):
    group_name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.group_name


# Grouped permissions
class GroupedPermission(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    group = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" % (self.group, str(self.permission))


# User permission
class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    has_permission = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.permission)


# Default permission
class DefaultPermission(models.Model):
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.permission
    
# Recieved Ducments
class ReceivedDocument(models.Model):
    memo = models.TextField()
    officeFrom = models.CharField(max_length=100)
    dateReceived = models.DateField()
    contactName = models.CharField(max_length=100 ,null=True, blank=True)
    contactNumber = models.CharField(max_length=15)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s/%s" % (self.contactNumber, self.contactName)

class FCMUserDeviceNotificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=8000)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (str(self.user), str(self.device_token))
