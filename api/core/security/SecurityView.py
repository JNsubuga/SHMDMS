from django.shortcuts import render

# Create your views here.
from .Security import Security
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
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.core.helper.helper import Helper
import json

DEFAULT_LANG = "en"

# init module class
_security = Security()
_helper = Helper()


class getAllSecurityGroups(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _security.getAllSecurityGroups(request, lang)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


# Get all tax location by id
class getAllSecurityGroupById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, securityid):
        lang = DEFAULT_LANG if lang == None else lang
        if not securityid:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        # get module
        results = _security.getAllSecurityGroupById(request, lang, securityid)
        if not (results == None):
            # if there is results
            return Response(results, status=200)
        else:
            return Response(
                {"message": "No Tax location is such ID", "success": False}, status=400
            )

    def post(self, request, lang, locationid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class CreateSecurityGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        if "group_name" in request.GET:
            if not request.GET["group_name"]:
                return Response(
                    {"message": "Role name is required", "success": False}, status=400
                )
            elif _security.SecurityGroupCodeNameExists(
                request, lang, request.GET["group_name"]
            ):
                return Response(
                    {
                        "message": "This role already exists, please note that your not allowed to update admin role",
                        "success": False,
                    },
                    status=400,
                )

            else:
                # get module
                group = _security.createSecurityGroup(
                    request, lang, request.GET["group_name"]
                )
                return Response(
                    {
                        "group": group,
                        "message": "Role created successfully",
                        "success": True,
                    },
                    status=200,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class UpdateSecurityGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, securityid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(securityid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        ######################
        if not str(securityid):
            return Response(
                {
                    "message": "Failed to update group, since all field are missing",
                    "success": False,
                },
                status=400,
            )
        if "group_name" in request.GET and "is_disabled" in request.GET:
            if not request.GET["group_name"] and not str(request.GET["is_disabled"]):
                return Response(
                    {
                        "message": "Failed to update group, since all field are missing",
                        "success": False,
                    },
                    status=400,
                )
            elif not _security.SecurityGroupExists(request, lang, securityid):
                return Response(
                    {"message": "Role doesn't exist", "success": False}, status=400
                )
            elif request.GET[
                "group_name"
            ] and _security.SecurityGroupCodeNameExistsByGroupId(
                request, lang, securityid, request.GET["group_name"]
            ):
                return Response(
                    {
                        "message": "This role already exists, please note that your not allowed to create admin role because its the system's default user",
                        "success": False,
                    },
                    status=400,
                )
            elif request.GET["group_name"] and _security.SecurityGroupIsAdmin(
                request, lang, securityid
            ):
                return Response(
                    {
                        "message": "please note that you are not allowed to create admin role because its the system's default user",
                        "success": False,
                    },
                    status=400,
                )
            ############################
            else:
                # get module
                group = _security.updateSecurityGroup(request, lang, securityid)
                return Response(
                    {
                        "group": group,
                        "message": "Security group updated secussfully",
                        "success": True,
                    },
                    status=202,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


# Get all tax location by id
class deleteSecurityGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, securityid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(securityid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        elif _security.SecurityGroupIsAdmin(request, lang, securityid):
            return Response(
                {
                    "message": "please note that your not allowed to delete or modify the Administration role",
                    "success": False,
                },
                status=400,
            )
        elif not _security.SecurityGroupExists(request, lang, securityid):
            return Response(
                {
                    "message": "Security group doesn't exists",
                    "success": False,
                },
                status=400,
            )
        # get module
        results = _security.deleteSecurityGroup(request, lang, securityid)
        if not (results == None):  # if there is results
            return Response(results, status=200)
        else:
            return Response(
                {"message": "Security group doesn't exists", "success": False},
                status=400,
            )

    def post(self, request, lang, securityid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getAllPermissions(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _security.getAllPermissions(request, lang)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


# Get all tax location by id
class getPermissionById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, permissionid):
        lang = DEFAULT_LANG if lang == None else lang
        if not permissionid:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        else:
            # get module
            results = _security.getPermissionById(request, lang, permissionid)
            return Response(results, status=200)

    def post(self, request, lang, permissionid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getAllUserPermissions(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        ##############################################
        token_auth = _helper.getAuthToken(request)
        if not token_auth["status"]:
            return Response(
                token_auth,
                status=400,
            )
        token = token_auth["token"]
        #############################################
        userid = Token.objects.get(key=token).user_id
        #############################################
        results = _security.getAllUserPermissions(request, lang, userid)
        return Response(
            {
                "permissions": results,
                "message": "",
                "success": True,
            },
            status=200,
        )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getUserPermissionById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, userpermid):
        lang = DEFAULT_LANG if lang == None else lang
        if not userpermid:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        # get module
        results = _security.getUserPermissionById(request, lang, userpermid)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getAllUserPermissionsByUserId(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        if not userid:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        # get module
        results = _security.getAllUserPermissionsByUserId(request, lang, userid)
        if not (results == None):
            # if there is results
            return Response(results, status=200)
        else:
            return Response(
                {"message": "No permission for this user", "success": False}, status=400
            )

    def post(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getPremitiveUserPermissionsByUserId(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        token = request.auth
        userid = Token.objects.get(key=token).user_id
        if not userid:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        all = (
            True
            if "all" not in request.GET or not str(request.GET["all"])
            else (True if (str(request.GET["all"]) == "true") else False)
        )
        # get module
        results = _security.getUserPermissionsByUserId(request, lang, userid, all)
        if not (results == None):
            # if there is results
            return Response(results, status=200)
        else:
            return Response(
                {"message": "No permissions for user", "success": False}, status=400
            )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class addPermissionToUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        token = request.auth
        userid = Token.objects.get(key=token).user_id
        if "permid" in request.GET:
            if not request.GET["permid"]:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
            permissionid = request.GET["permid"]
            if not _security.PermissionExists(request, lang, permissionid):
                return Response(
                    {"message": "Permission doesn't exists", "success": False},
                    status=400,
                )

            if _security.userHasPermission(
                request, lang, request.GET["permid"], userid
            ):
                return Response(
                    {"message": "User already has permission", "success": False},
                    status=400,
                )
            # get module
            results = _security.addPermissionToUser(request, lang, userid)
            if results:
                # if there is results
                return Response(
                    {"message": "Permission add secussfully", "success": True},
                    status=200,
                )
            else:
                return Response({"message": "", "success": False}, status=400)
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang, permissionid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class removePermissionFromUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        token = request.auth
        userid = Token.objects.get(key=token).user_id
        if "permid" in request.GET:
            if not request.GET["permid"]:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
            if not _security.userHasPermission(
                request, lang, request.GET["permid"], userid
            ):
                return Response(
                    {"message": "This user has no such permission", "success": False},
                    status=400,
                )
            permid = int(request.GET["permid"])
            # get module
            results = _security.removePermissionFromUser(request, lang, userid, permid)
            if results:
                # if there is results
                return Response(
                    {"message": "Permission removed succesfully", "success": True},
                    status=200,
                )
            else:
                return Response({"message": "", "success": False}, status=400)
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class addPermissionsToUserInBatch(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        ##############################################
        token_auth = _helper.getAuthToken(request)
        if not token_auth["status"]:
            return Response(
                token_auth,
                status=400,
            )
        token = token_auth["token"]
        #############################################
        userid = Token.objects.get(key=token).user_id
        #############################################
        ########################3
        if request.data:
            data = request.data
            if len(data) > 0:
                _security.addPermissionToUserInBatch(request, lang, userid, data)
                return Response(
                    {"message": "Permissions granted succefully", "success": True},
                    status=200,
                )
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


class removePermissionsFromUserInBatch(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        #############
        token = request.auth
        userid = Token.objects.get(key=token).user_id
        ##############
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if len(data) > 0:
                _security.removePermissionsFromUserInBatch(request, lang, userid, data)
                return Response(
                    {"message": "Permissions removed succefully", "success": True},
                    status=200,
                )
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


class CreatePermissionGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        if "group_name" in request.GET:
            if not request.GET["group_name"]:
                return Response(
                    {"message": "Permission group name is required", "success": False},
                    status=400,
                )
            else:
                # get module
                results = _security.createPermissionGroup(
                    request, lang, request.GET["group_name"]
                )
                return Response(
                    {
                        "message": "Permission group created successfully",
                        "success": True,
                    },
                    status=200,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang, permissionid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class UpdatePermissionGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(groupid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        elif not _security.PermissionGroupExsists(request, lang, groupid):
            return Response(
                {"message": "Permission group doesn't exist", "success": False},
                status=400,
            )
        ##################################################
        if not str(groupid):
            return Response(
                {
                    "message": "Failed to update group, since all field are missing",
                    "success": False,
                },
                status=400,
            )
        if "group_name" in request.GET and "is_disabled" in request.GET:
            if not request.GET["group_name"] and not str(request.GET["is_disabled"]):
                return Response(
                    {
                        "message": "Failed to update group, since all field are missing",
                        "success": False,
                    },
                    status=400,
                )
            else:
                # get module
                _security.UpdatePermissionGroup(request, lang, groupid)
                return Response(
                    {
                        "message": "Permission group updated secussfully",
                        "success": True,
                    },
                    status=200,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getAllPermissionGroups(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _security.getAllPermissionGroups(request, lang)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getPermissionGroupById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if not _security.PermissionGroupExsists(request, lang, groupid):
            return Response(
                {"message": "Permission group doesn't exist", "success": False},
                status=400,
            )
        results = _security.getPermissionGroupById(request, lang, groupid)
        return Response(results, status=200)

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class DeletePermission(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if not _security.PermissionGroupExsists(request, lang, groupid):
            return Response(
                {"message": "Permission group doesn't exist", "success": False},
                status=400,
            )
        _security.DeletePermission(request, lang, groupid)
        return Response(
            {"message": "Permission deleted successfully", "success": False}, status=200
        )

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class addPermissionToGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if "permid" in request.GET:
            if not groupid and not request.GET["permid"]:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
            if _security.PermissionExistsInGroup(
                request, lang, groupid, int(request.GET["permid"])
            ):
                return Response(
                    {
                        "message": "Permission already exists in this group",
                        "success": False,
                    },
                    status=400,
                )
            # get module
            permid = int(request.GET["permid"])
            results = _security.addPermissionToGroup(request, lang, groupid, permid)
            if results:
                # if there is results
                return Response(
                    {"message": "Permission added successfully", "success": True},
                    status=200,
                )
            else:
                return Response({"message": "", "success": False}, status=400)
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )

    def post(self, request, lang, permissionid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class addPermissionsToGroupInBatch(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if request.data:
            data = request.data
            if len(data) > 0:
                _security.addPermissionToGroupInBatch(request, lang, groupid, data)
                return Response(
                    {"message": "Permissions added succefully", "success": True},
                    status=200,
                )
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


class getAllPermissionsByGroups(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _security.getAllPermissionsByGroups(request, lang)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getPermissionsByGroupId(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(groupid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        results = _security.getPermissionsByGroupId(request, lang, groupid)
        return Response(results, status=200)

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class removePermissionsFromGroupInBatch(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if len(data) > 0:
                _security.removePermissionToGroupInBatch(request, lang, groupid, data)
                return Response(
                    {"message": "Permissions removed succefully", "success": True},
                    status=200,
                )
            else:
                return Response(
                    {"message": "No permissions selected", "success": False}, status=400
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


############################################# DEFAULT PERMISSIONS MANAGEMENT ##########################
class addDefaultPermissionsInBatch(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if request.data:
            data = request.data
            if len(data) > 0:
                _security.addRemoveDefaultPermissionsInBatch(
                    request, lang, groupid, data
                )
                return Response(
                    {"message": "Permissions added succefully", "success": True},
                    status=200,
                )
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False}, status=400
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


class getAllDefaultPermissions(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _security.getAllPermissionsByGroups(request, lang)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getDefaultPermissionById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(groupid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        results = _security.getPermissionsByGroupId(request, lang, groupid)
        return Response(results, status=200)

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class removeDefaultPermissionsInBatch(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if len(data) > 0:
                _security.removeDefaultPermissionsInBatch(request, lang, data)
                return Response(
                    {"message": "Permissions removed succefully", "success": True},
                    status=200,
                )
            else:
                return Response(
                    {"message": "No permissions selected", "success": False}, status=400
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


class getAllSecurityGroupPermissions(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _security.getAllSecurityGroupPermissions(request, lang)
        return Response(results, status=200)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )


class getAllSecurityGroupPermissionById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(groupid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        results = _security.getAllSecurityGroupPermissionsById(request, lang, groupid)
        return Response(results, status=200)

    def post(self, request, lang, groupid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {"message": "Invalid request method", "success": False}, status=400
        )
