# Create your views here.
from email.policy import default
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from api.core.helper import helper, webconfig
from api.models import *
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ObjectDoesNotExist
from operator import itemgetter
from api.core.locale.Locale import Locale


# master module class
class Security:
    def __init__(self):
        self.help = helper.Helper()
        self.locale = Locale()

        # Get All Modules

    def getAllSecurityGroups(self, request, lang):
        results = []
        groups = SecurityGroup.objects.filter(is_disabled=False).order_by("-id")
        for group in groups:
            group_name = getattr(group, f"{lang}_group_name")
            results.append(
                {
                    "group_id": group.pk,
                    "group_name": group_name,
                    "code_name": group.code_name,
                    "created": group.created,
                    "is_disabled": group.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    def getAllSecurityGroupById(self, request, lang, securityid):
        group = SecurityGroup.objects.filter(
            Q(is_disabled=False) and Q(pk=securityid)
        ).get()
        group_name = getattr(group, f"{lang}_group_name")
        return {
            "group_id": group.pk,
            "group_name": group_name,
            "code_name": group.code_name,
            "created": group.created,
            "is_disabled": group.is_disabled,
            "message": "",
            "success": True,
        }

    def SecurityGroupCodeNameExistsByGroupId(
        self, request, lang, securityid, groupname
    ):
        groupcodename = groupname.lower().replace(" ", "_")
        return (
            SecurityGroup.objects.filter(~Q(pk=int(securityid)))
            .filter(code_name=groupcodename)
            .exists()
        )

    def SecurityGroupCodeNameExists(self, request, lang, groupname):
        groupcodename = groupname.lower().replace(" ", "_")
        return SecurityGroup.objects.filter(code_name=groupcodename).exists()

    def SecurityGroupIsAdmin(self, request, lang, security_group_id):
        return (
            SecurityGroup.objects.filter(pk=security_group_id)
            .filter(code_name="admin")
            .exists()
        )

    def SecurityGroupExists(self, request, lang, security_group_id):
        return SecurityGroup.objects.filter(pk=security_group_id).exists()

    def createSecurityGroup(self, request, lang, groupname):
        new_group_name = groupname.lower().replace(" ", "_")
        update = {
            f"{lang}_group_name": groupname,
            "code_name": new_group_name,
        }
        securitygroup = SecurityGroup.objects.create(**update)
        securitygroup.save()
        return self.getAllSecurityGroupById(request, lang, securitygroup.pk)

    def updateSecurityGroup(self, request, lang, securitygroupid):
        security_group = SecurityGroup.objects.filter(pk=securitygroupid).get()
        old_group_name = getattr(security_group, f"{lang}_group_name")
        groupname = (
            request.GET["group_name"] if request.GET["group_name"] else old_group_name
        )
        is_disabled = (
            True
            if request.GET["is_disabled"] == "true"
            else (
                False if str(request.GET["is_disabled"]) else security_group.is_disabled
            )
        )
        new_group_name = groupname.lower().replace(" ", "_")
        update_dict = {
            f"{lang}_group_name": groupname,
            "code_name": new_group_name,
            "is_disabled": is_disabled,
        }
        securitygroup = SecurityGroup.objects.filter(pk=securitygroupid)
        securitygroup.update(**update_dict)
        return self.getAllSecurityGroupById(request, lang, securitygroupid)

    def disableSecurityGroup(self, request, lang, securityid):
        SecurityGroup.objects.filter(pk=securityid).update(
            is_disabled=True,
            has_been_modified=True,
            last_modified=self.help.getDateTime(),
        )

    def SecurityGroupHasBeenUsed(self, request, lang, securityid):
        usergroup = UserGroup.objects.filter(
            security_group=SecurityGroup(pk=securityid)
        ).exists()
        defaultpermission = DefaultPermission.objects.filter(
            security_group=SecurityGroup(pk=securityid)
        ).exists()
        if usergroup or defaultpermission:
            return True
        else:
            return False

    def deleteSecurityGroup(self, request, lang, securityid):
        # First check if these modules exist
        if SecurityGroup.objects.filter(pk=securityid):
            if self.SecurityGroupHasBeenUsed(request, lang, securityid):
                self.disableSecurityGroup(request, lang, securityid)
            else:
                department = SecurityGroup.objects.filter(pk=securityid).get()
                department.delete()
            return {
                "message": f"Security group deleted succesfully",
                "status": "success",
            }
        else:
            return None

    def getAuthUserById(self, request, lang, userid):
        user = User.objects.get(pk=userid)
        profile = UserProfile.objects.get(user=User(pk=userid))
        token, created = Token.objects.get_or_create(user=user)
        profile = UserProfile.objects.get(user=User(pk=userid))
        group = UserGroup.objects.get(user=User(pk=userid))
        group_name = getattr(group.security_group, f"{lang}_group_name")
        permissions = self.getUserPermissionsByUserId(request, lang, userid)
        return {
            "id": user.pk,
            "token": str(token),  # None
            "username": user.username,  # `django.contrib.auth.User` instance.
            "email": user.email,
            "is_superuser": user.is_superuser,
            "group": {
                "id": group.security_group.pk,
                "group_name": group_name,
                "group_code_name": group.security_group.code_name,
                "permissions": permissions,
            },
            "last_login": user.last_login,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile": {
                "id": user.pk,
                "gender": profile.gender,
                "phoneno": profile.phoneno,
                "address": profile.address,
                "birth_date": profile.birth_date,
                "photo": f"{webconfig.API_URL}/media/{profile.photo}",
                "is_editable": profile.is_editable,
                "is_deletable": profile.is_deletable,
                "is_disabled": profile.is_disabled,
                "created": profile.created,
            },
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            "message": "",
            "success": True,
        }

    # Get All Permissions
    def getAllPermissions(self, request, lang):
        results = []
        permissions = Permission.objects.filter(is_disabled=False).order_by("-id")
        # module is compulsory
        for permission in permissions:
            permission_name = getattr(permission, f"{lang}_permission_name")
            # print(module_name)
            results.append(
                {
                    "permission_id": permission.pk,
                    "permission_name": permission_name,
                    "code_name": permission.code_name,
                    "created": permission.created,
                    "has_been_modified": permission.has_been_modified,
                    "is_disabled": permission.is_disabled,
                    "last_modified": permission.last_modified,
                    "message": "",
                    "success": True,
                }
            )
        return results

    # Get permission by id
    def getPermissionById(self, request, lang, permissionid):
        permission = Permission.objects.filter(pk=permissionid).get()
        permission_name = getattr(permission, f"{lang}_permission_name")
        return {
            "permission_id": permission.pk,
            "permission_name": permission_name,
            "code_name": permission.code_name,
            "created": permission.created,
            "has_been_modified": permission.has_been_modified,
            "is_disabled": permission.is_disabled,
            "last_modified": permission.last_modified,
            "message": "",
            "success": True,
        }

    def getAllUserPermissionsGroups(self, request, lang):
        results = []
        permission_groups = UserPermission.objects.values("user").annotate(
            dcount=Count("user")
        )
        # module is compulsory
        for permission_group in permission_groups:
            user = self.getAuthUserById(request, lang, permission_group["user"])
            uresults = []
            upermissions = (
                UserPermission.objects.filter(has_permission=True)
                .filter(
                    Q(is_disabled=False) and Q(user=User(pk=permission_group["user"]))
                )
                .order_by("-id")
            )
            # module is compulsory
            for upermission in upermissions:
                permission = self.getPermissionById(
                    request, lang, upermission.permission.pk
                )
                uresults.append(permission)
            user["permission"] = uresults
            results.append(user)
        return results

    def getAllUserPermissions(self, request, lang, userid):
        results = []
        upermissions = (
            UserPermission.objects.filter(user=User(pk=userid))
            .filter(has_permission=True)
            .filter(is_disabled=False)
            .order_by("-id")
        )
        # module is compulsory
        for upermission in upermissions:
            permission = self.getPermissionById(
                request, lang, upermission.permission.pk
            )
            results.append(
                {
                    "id": upermission.pk,
                    "permission": permission,
                    "has_permission": upermission.has_permission,
                    "created": upermission.created,
                    "is_disabled": upermission.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    def getAllUserPermissionGroups(self, request, lang):
        results = []
        permission_groups = UserPermission.objects.values("user").annotate(
            dcount=Count("user")
        )
        # module is compulsory
        for permission_group in permission_groups:
            user = self.getAuthUserById(request, lang, permission_group["user"])
            uresults = []
            upermissions = UserPermission.objects.filter(
                Q(is_disabled=False) and Q(user=User(pk=permission_group["user"]))
            ).order_by("-id")
            # module is compulsory
            for upermission in upermissions:
                permission = self.getPermissionById(
                    request, lang, upermission.permission.pk
                )
                uresults.append(permission)
            user["permission"] = uresults
            results.append(user)
        return results

    def getAllUserPermission(self, request, lang):
        results = []
        upermissions = UserPermission.objects.filter(is_disabled=False).order_by("-id")
        # module is compulsory
        for upermission in upermissions:
            user = self.getAuthUserById(request, lang, upermission.user.pk)
            permission = self.getPermissionById(
                request, lang, upermission.permission.pk
            )
            results.append(
                {
                    "id": upermission.pk,
                    "user": user,
                    "permission": permission,
                    "is_disabled": upermission.is_disabled,
                    "message": "",
                    "success": True,
                    "created": upermission.created,
                }
            )
        return results

    def getUserPermissionsByUserId(self, request, lang, userid, all=True):
        results = []
        if all:
            permissions = Permission.objects.filter(is_disabled=False).order_by("-id")
            # module is compulsory
            for permission in permissions:
                permission_name = getattr(permission, f"{lang}_permission_name")
                has_permission = (
                    UserPermission.objects.filter(user=User(pk=userid))
                    .filter(permission=Permission(pk=permission.pk))
                    .filter(has_permission=True)
                    .filter(is_disabled=False)
                    .exists()
                )
                results.append(
                    {
                        "permission_id": permission.pk,
                        "permission_name": permission_name,
                        "code_name": permission.code_name,
                        "has_permission": has_permission,
                        "created": permission.created,
                        "has_been_modified": permission.has_been_modified,
                        "is_disabled": permission.is_disabled,
                        "last_modified": permission.last_modified,
                        "message": "",
                        "success": True,
                    }
                )
            newlist = sorted(results, key=itemgetter("has_permission"), reverse=True)
            return newlist
        else:
            userpermissions = (
                UserPermission.objects.filter(user=User(pk=userid))
                .filter(has_permission=True)
                .filter(is_disabled=False)
            )
            for userpermission in userpermissions:
                permission = userpermission.permission
                permission_name = getattr(permission, f"{lang}_permission_name")
                results.append(
                    {
                        "permission_id": permission.pk,
                        "permission_name": permission_name,
                        "code_name": permission.code_name,
                        "has_permission": userpermission.has_permission,
                        "created": permission.created,
                        "has_been_modified": permission.has_been_modified,
                        "is_disabled": permission.is_disabled,
                        "last_modified": permission.last_modified,
                        "message": "",
                        "success": True,
                    }
                )
            newlist = sorted(results, key=itemgetter("has_permission"), reverse=True)
            return newlist

    def getUserPermissionById(self, request, lang, userpermid):
        upermission = UserPermission.objects.filter(
            Q(is_disabled=False) and Q(pk=userpermid)
        ).get()
        permission = self.getPermissionById(request, lang, upermission.permission.pk)
        return {
            "id": upermission.pk,
            "permission": permission,
            "created": upermission.created,
            "has_permission": upermission.has_permission,
            "is_disabled": upermission.is_disabled,
            "message": "",
            "success": True,
        }

    def getAllUserPermissionsByUserId(self, request, lang, userid):
        results = []
        upermissions = (
            UserPermission.objects.filter(user=User(pk=userid))
            .filter(is_disabled=False)
            .filter(has_permission=True)
            .order_by("-id")
        )
        # module is compulsory
        for upermission in upermissions:
            user = self.getAuthUserById(request, lang, upermission.user.pk)
            permission = self.getPermissionById(
                request, lang, upermission.permission.pk
            )
            results.append(
                {
                    "id": upermission.pk,
                    "user": user,
                    "permission": permission,
                    "created": upermission.created,
                    "is_disabled": upermission.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    def userHasPermission(self, request, lang, permid, userid):
        return (
            UserPermission.objects.filter(user=User(pk=userid))
            .filter(permission=Permission(pk=permid))
            .exists()
        )

    def PermissionExists(self, request, lang, permid):
        return Permission.objects.filter(pk=int(permid)).exists()

    def addPermissionToUser(self, request, lang, userid):
        permid = request.GET["permid"]
        upermission = UserPermission.objects.create(
            user=User(pk=userid),
            permission=Permission(pk=permid),
        )
        upermission.save()
        return True

    def removePermissionFromUser(self, request, lang, userid, permid):
        upermission = UserPermission.objects.filter(
            Q(user=User(pk=userid)) and Q(permission=Permission(pk=permid))
        )
        upermission.delete()
        return True

    def addPermissionToUserInBatch(self, request, lang, userid, data):

        for permid in data:
            if self.PermissionExists(request, lang, permid):

                if not self.userHasPermission(request, lang, permid, userid):
                    upermission = UserPermission.objects.create(
                        user=User(pk=userid), permission=Permission(pk=permid)
                    )
                    upermission.save()
                else:
                    print(permid)
                    upermission = (
                        UserPermission.objects.filter(user=User(pk=userid))
                        .filter(permission=Permission(pk=permid))
                        .update(
                            has_permission=True,
                        )
                    )
        # delete other persmissions that are not in the list
        UserPermission.objects.filter(user=User(pk=userid)).filter(
            ~Q(permission__id__in=data)
        ).delete()
        ################3
        return True

    def removePermissionsFromUserInBatch(self, request, lang, userid, data):
        for permid in data:
            if self.userHasPermission(request, lang, permid, userid):
                # Update permission status if it exists
                UserPermission.objects.filter(user=User(pk=userid)).filter(
                    permission=Permission(pk=permid)
                ).update(
                    has_permission=False,
                )
        return True

    def createPermissionGroup(self, request, lang, groupname):
        new_group_name = groupname.lower().replace(" ", "_")
        permissiongroup = PermissionGroup.objects.create(
            group_name=groupname,
            code_name=new_group_name,
        )
        permissiongroup.save()
        return True

    def UpdatePermissionGroup(self, request, lang, groupid):
        permissiongroup = PermissionGroup.objects.filter(pk=int(groupid)).get()
        group_name = (
            request.GET["group_name"]
            if str(request.GET["group_name"])
            else permissiongroup.group_name
        )
        is_disabled = (
            True
            if request.GET["is_disabled"] == "true"
            else (
                False
                if str(request.GET["is_disabled"])
                else permissiongroup.is_disabled
            )
        )
        new_group_name = group_name.lower().replace(" ", "_")
        permissiongroup = PermissionGroup.objects.filter(pk=int(groupid)).update(
            group_name=group_name, is_disabled=is_disabled, code_name=new_group_name
        )
        return True

        # Get All Modules

    def getAllPermissionGroups(self, request, lang):
        results = []
        permission_groups = PermissionGroup.objects.filter(is_disabled=False).order_by(
            "-id"
        )
        # module is compulsory
        for permission_group in permission_groups:
            # print(module_name)
            results.append(
                {
                    "group_id": permission_group.pk,
                    "group_name": permission_group.group_name,
                    "code_name": permission_group.code_name,
                    "created": permission_group.created,
                    "is_disabled": permission_group.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    def PermissionGroupExsists(self, request, lang, groupid):
        return PermissionGroup.objects.filter(pk=groupid).exists()

    def PermissionExistsInGroup(self, request, lang, groupid, permid):
        return (
            GroupedPermission.objects.filter(permission=Permission(pk=int(permid)))
            .filter(group=PermissionGroup(pk=groupid))
            .exists()
        )

        # Get All Modules

    def getPermissionGroupById(self, request, lang, groupid):
        permission_group = PermissionGroup.objects.filter(pk=groupid).get()
        # module is compulsory
        return {
            "group_id": permission_group.pk,
            "group_name": permission_group.group_name,
            "code_name": permission_group.code_name,
            "created": permission_group.created,
            "is_disabled": permission_group.is_disabled,
            "message": "",
            "success": True,
        }

    def DeletePermission(self, request, lang, groupid):
        permission_group = PermissionGroup.objects.filter(pk=groupid).get()
        permission_group.delete()
        return True

    def addPermissionToGroup(self, request, lang, groupid, permid):
        if self.PermissionExists(request, lang, permid):
            groupedpermissions = GroupedPermission.objects.create(
                permission=Permission(pk=permid),
                group=PermissionGroup(pk=groupid),
            )
            groupedpermissions.save()
        return True

    def addPermissionToGroupInBatch(self, request, lang, groupid, data):
        for permid in data:
            if not self.PermissionExistsInGroup(request, lang, groupid, permid):
                if self.PermissionExists(request, lang, permid):
                    groupedpermissions = GroupedPermission.objects.create(
                        permission=Permission(pk=permid),
                        group=PermissionGroup(pk=groupid),
                    )
                    groupedpermissions.save()
        return True

    # Get All Modules
    def getAllPermissionsByGroups(self, request, lang):
        results = []
        permission_groups = PermissionGroup.objects.filter(is_disabled=False).order_by(
            "-id"
        )
        # module is compulsory
        for permission_group in permission_groups:
            mpermission = []
            groupedpermissions = GroupedPermission.objects.filter(
                group=PermissionGroup(pk=permission_group.pk)
            )
            #####################################
            for groupedpermission in groupedpermissions:
                permissionid = groupedpermission.permission.pk
                permission = self.getPermissionById(request, lang, permissionid)
                mpermission.append(permission)
            # print(module_name)
            results.append(
                {
                    "group_id": permission_group.pk,
                    "group_name": permission_group.group_name,
                    "permission": mpermission,
                    "code_name": permission_group.code_name,
                    "created": permission_group.created,
                    "is_disabled": permission_group.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    # Get All Modules
    def getPermissionsByGroupId(self, request, lang, groupid):
        permission_group = PermissionGroup.objects.filter(pk=groupid).get()
        mpermission = []
        groupedpermissions = GroupedPermission.objects.filter(
            group=PermissionGroup(pk=permission_group.pk)
        )
        #####################################
        for groupedpermission in groupedpermissions:
            permissionid = groupedpermission.permission.pk
            permission = self.getPermissionById(request, lang, permissionid)
            mpermission.append(permission)
        return {
            "group_id": permission_group.pk,
            "group_name": permission_group.group_name,
            "permission": mpermission,
            "code_name": permission_group.code_name,
            "created": permission_group.created,
            "is_disabled": permission_group.is_disabled,
            "message": "",
            "success": True,
        }

    def removePermissionToGroupInBatch(self, request, lang, groupid, data):
        for permid in data:
            if self.PermissionExistsInGroup(request, lang, groupid, permid):
                groupedpermission = GroupedPermission.objects.filter(
                    permission=Permission(pk=int(permid))
                ).filter(group=PermissionGroup(pk=groupid))
                groupedpermission.delete()
        return True

    def PermissionExistsInDefault(self, request, lang, groupid, permid):
        return (
            DefaultPermission.objects.filter(permission=Permission(pk=int(permid)))
            .filter(security_group=SecurityGroup(pk=groupid))
            .exists()
        )

    def PermissionExistsInDefaultPrev(self, request, lang, defpermid):
        return DefaultPermission.objects.filter(pk=defpermid).exists()

    def addRemoveDefaultPermissionsInBatch(self, request, lang, groupid, data):
        for permid in data:
            if not self.PermissionExistsInDefault(request, lang, groupid, permid):
                if self.PermissionExists(request, lang, permid):
                    defaultpermission = DefaultPermission.objects.create(
                        permission=Permission(pk=permid),
                        security_group=SecurityGroup(pk=groupid),
                    )
                    defaultpermission.save()
        # delete other persmissions that are not in the list
        DefaultPermission.objects.filter(
            security_group=SecurityGroup(pk=groupid)
        ).filter(~Q(permission__id__in=data)).delete()
        ################3
        return True

        # Get All Modules

    def getAllSecurityGroupPermissions(self, request, lang):
        results = []
        defaultpermissions = (
            DefaultPermission.objects.values("is_disabled", "security_group_id")
            .annotate(count=Count("security_group_id"))
            .order_by()
        )
        for defaultpermission in defaultpermissions:
            security_group_id = defaultpermission["security_group_id"]
            security_group = self.getAllSecurityGroupById(
                request, lang, security_group_id
            )
            spermissions = DefaultPermission.objects.filter(
                security_group=SecurityGroup(pk=security_group_id)
            ).order_by("-id")
            permissions = []
            for spermission in spermissions:
                perm = self.getPermissionById(request, lang, spermission.permission.pk)
                perm["defpermid"] = spermission.pk
                permissions.append(perm)
            security_group["permissions"] = permissions
            results.append(security_group)
        return results

    # Get security group permissions by id
    def getAllSecurityGroupPermissionsById(self, request, lang, groupid):
        security_group = self.getAllSecurityGroupById(request, lang, groupid)
        spermissions = DefaultPermission.objects.filter(
            security_group=SecurityGroup(pk=groupid)
        )
        permissions = []
        for spermission in spermissions:
            perm = self.getPermissionById(request, lang, spermission.permission.pk)
            perm["defpermid"] = spermission.pk
            permissions.append(perm)
        security_group["permissions"] = permissions
        return security_group

    def removeDefaultPermissionsInBatch(self, request, lang, data):
        for defpermid in data:
            if self.PermissionExistsInDefaultPrev(request, lang, defpermid):
                defperm = DefaultPermission.objects.filter(pk=defpermid)
                defperm.delete()
        return True
