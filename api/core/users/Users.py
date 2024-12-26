from django.shortcuts import render

# Create your views here.
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
from api.core.security.Security import Security
from api.models import *
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from api.core.gender.Genders import Genders
import json


# master module class
class Users:
    def __init__(self):
        self.help = helper.Helper()
        self.security = Security()
        self.gender = Genders()

    def getAuthUser(self, request, lang, userid):
        user = User.objects.get(pk=userid)
        profile = UserProfile.objects.get(user=User(pk=userid))
        group = UserGroup.objects.get(user=User(pk=userid))
        group_name = getattr(group.security_group, f"{lang}_group_name")
        permissions = self.security.getUserPermissionsByUserId(request, lang, userid)
        token, created = Token.objects.get_or_create(user=user)
        ############################################################################
        return {
            "id": userid,
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
                "id": profile.pk,
                "gender": (
                    self.gender.getGenderById(request, lang, profile.gender.pk)
                    if not (profile.gender == None)
                    else None
                ),
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

    def getAuthUserById(self, request, lang, userid):
        user = User.objects.get(pk=userid)
        profile = UserProfile.objects.get(user=User(pk=userid))
        token, created = Token.objects.get_or_create(user=user)
        profile = UserProfile.objects.get(user=User(pk=userid))
        group = UserGroup.objects.get(user=User(pk=userid))
        group_name = getattr(group.security_group, f"{lang}_group_name")
        permissions = self.security.getUserPermissionsByUserId(request, lang, userid)
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
                "gender": (
                    self.gender.getGenderById(request, lang, profile.gender.pk)
                    if not (profile.gender == None)
                    else None
                ),
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

    def getAllUsers(self, request, lang):
        results = []
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            userid = user.pk
            token, created = Token.objects.get_or_create(user=user)
            profile = UserProfile.objects.get(user=User(pk=userid))
            group = UserGroup.objects.get(user=User(pk=userid))
            group_name = getattr(group.security_group, f"{lang}_group_name")
            permissions = self.security.getUserPermissionsByUserId(
                request, lang, userid
            )
            results.append(
                {
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
                        "gender": (
                            self.gender.getGenderById(request, lang, profile.gender.pk)
                            if not (profile.gender == None)
                            else None
                        ),
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
            )
        return results

    def EmailOrUsernameLogin(self, request, lang, username):
        users = User.objects.filter(Q(username=username) | Q(email=username))
        if users.exists():
            user = users.get()
            userid = user.pk
            return self.getAuthUserById(request, lang, userid)
        else:
            return {"message": "Invalid login credentials", "success": False}

    def accountExists(self, request, lang):
        user = User.objects.filter(username=request.data["username"])
        if user:
            return True
        else:
            return False

    def userExists(self, request, lang, userid):
        return User.objects.filter(pk=userid).exists()

    def emailExists(self, request, lang, email):
        return User.objects.filter(email=email).exists()

    def emailExistsByUserId(self, request, lang, userid, email):
        return User.objects.filter(~Q(pk=userid)).filter(email=email).exists()

    def createAuthUser(self, request, lang, data):
        #############################################
        current_datetime = datetime.now()
        username = data["username"]
        first_name = data["first_name"]
        security_group_id = data["security_group_id"]
        sgroup = self.security.getAllSecurityGroupById(
            request, lang, int(security_group_id)
        )
        sgcodename = sgroup["code_name"]
        email = data["email"]
        last_name = data["last_name"]
        password = data["password"]
        password = str("123456") if not password else password
        is_staff = data["is_staff"]
        is_superuser = (
            data["is_superuser"]
            if str(data["is_superuser"])
            else (True if (sgcodename == "admin" or sgcodename == "owner") else False)
        )
        # PROFILE
        profile = data["profile"]
        gender = int(profile["gender"]) if str(profile["gender"]) else None
        phoneno = profile["phoneno"]
        bio = profile["bio"]
        address = profile["address"]
        birth_date = profile["birth_date"] if profile["birth_date"] else None
        photo = profile["photo"] if profile["photo"] else "default_profile.jpg"
        # create user
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = True
        user.save()
        # get saved user
        userid = user.pk
        usergroup = UserGroup(
            user=User(pk=userid),
            security_group=SecurityGroup(pk=security_group_id),
            last_modified=current_datetime,
        )
        usergroup.save()
        # Get the user add update the available profile data
        uuser = User.objects.get(pk=userid)
        uuser.userprofile.gender = Gender(pk=gender)
        uuser.userprofile.phoneno = phoneno
        uuser.userprofile.address = address
        uuser.userprofile.birth_date = birth_date
        uuser.userprofile.photo = photo
        uuser.save()
        # get Token
        token, created = Token.objects.get_or_create(user=User(pk=userid))
        return {
            "token": token.key,
            "username": username,
            "user_id": userid,
            "password": password,
            "email": email,
            "message": "User successfully with new password " + password,
            "success": True,
        }

    def UpdateAuthUserPassword(self, request, lang, password, userid):
        password = make_password(str(password))
        old_user = User.objects.filter(pk=userid)
        old_user.update(password=password)
        return True

    def UpdateAuthUser(self, request, lang, userid, data):
        current_datetime = datetime.now()
        old_user = User.objects.filter(pk=userid).get()
        old_usergroup = UserGroup.objects.filter(user=User(pk=userid)).get()
        new_password = data["new_password"]
        username = data["username"] if data["username"] else old_user.username
        first_name = data["first_name"] if data["first_name"] else old_user.first_name
        email = data["email"] if data["email"] else old_user.email
        last_name = data["last_name"] if data["last_name"] else old_user.last_name
        is_staff = data["is_staff"] if str(data["is_staff"]) else old_user.is_staff
        is_superuser = (
            data["is_superuser"] if str(data["is_superuser"]) else old_user.is_superuser
        )
        is_active = data["is_active"] if str(data["is_active"]) else old_user.is_active
        # PROFILE
        gender = data["gender"] if data["gender"] else old_user.userprofile.gender.pk
        phoneno = data["phoneno"] if data["phoneno"] else old_user.userprofile.phoneno
        address = data["address"] if data["address"] else old_user.userprofile.address
        birth_date = (
            data["birth_date"]
            if data["birth_date"]
            else old_user.userprofile.birth_date
        )
        photo = data["photo"] if data["photo"] else old_user.userprofile.photo
        security_group_id = (
            data["security_group_id"]
            if str(data["security_group_id"])
            else old_usergroup.security_group.pk
        )
        is_editable = (
            data["is_editable"]
            if str(data["is_editable"])
            else old_user.userprofile.is_editable
        )
        is_deletable = (
            data["is_deletable"]
            if str(data["is_deletable"])
            else old_user.userprofile.is_deletable
        )

        uuser = User.objects.get(pk=userid)
        uuser.username = username
        uuser.first_name = first_name
        uuser.email = email
        uuser.last_name = last_name
        uuser.is_staff = is_staff
        uuser.is_superuser = is_superuser
        uuser.is_active = is_active
        uuser.userprofile.gender = Gender(pk=gender)
        uuser.userprofile.phoneno = phoneno
        ################################################
        uuser.userprofile.is_editable = is_editable
        uuser.userprofile.is_deletable = is_deletable
        ######################################
        uuser.userprofile.address = address
        uuser.userprofile.birth_date = birth_date
        uuser.userprofile.photo = photo
        uuser.save()
        # create user
        usergroup = UserGroup.objects.filter(user=User(pk=userid))
        usergroup.update(
            security_group=SecurityGroup(pk=security_group_id),
            has_been_modified=True,
            last_modified=current_datetime,
        )
        if str(new_password) and len(new_password) >= 6:
            self.UpdateAuthUserPassword(request, lang, new_password, userid)
        return True
