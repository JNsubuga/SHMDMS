from django.shortcuts import render

# Create your views here.
from .Users import Users
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
from api.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.core.helper.helper import Helper
import json

DEFAULT_LANG = "en"

# init module class
_users = Users()
_helper = Helper()


class GetAuthUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

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
        user = _users.getAuthUser(request, lang, userid)
        return Response(user)


class GetAllUsers(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getAllUsers(request, lang)
        return Response(user)


class GetAuthUserById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(userid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        elif not _users.userExists(request, lang, userid):
            return Response(
                {"message": "User doesn't exist", "success": False}, status=400
            )
        user = _users.getAuthUserById(request, lang, userid)
        return Response(user)


# Login User
class LoginUser(APIView):
    authentication_classes = ()  # disable token authentication for login
    permission_classes = ()
    http_method_names = ["post"]

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        ##################################################
        data = request.data
        if data:
            # data = json.loads(request_object)
            if data:
                if "username" in data and "password" in data:
                    username = data["username"]
                    password = data["password"]
                    if not username:
                        return Response(
                            {"message": "Username is required", "success": False}
                        )
                    elif not password:
                        return Response(
                            {
                                "message": "Password is required",
                                "success": False,
                            }
                        )
                    else:
                        login = _users.EmailOrUsernameLogin(request, lang, username)
                        if not login["success"]:
                            return Response(login)
                        else:
                            user = authenticate(username=username, password=password)
                            if user:
                                token, created = Token.objects.get_or_create(user=user)
                                return Response(
                                    {
                                        "token": token.key,
                                        "user_id": user.pk,
                                        "message": "",
                                        "success": True,
                                    }
                                )
                            else:
                                return Response(
                                    {
                                        "message": "Invalid login credentials",
                                        "success": False,
                                    }
                                )
                else:
                    return Response(
                        {"message": "Incomplete data request", "success": False},
                        status=400,
                    )
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False},
                    status=400,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


# Generate custom AUTH Token
class CreateUserAuthToken(ObtainAuthToken):
    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


# Create Auth User
class CreateAuthUser(ObtainAuthToken):
    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        ##################################################
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if data:
                username = data["username"]
                first_name = data["first_name"]
                last_name = data["last_name"]
                password = data["password"]
                confirmpassword = data["confirmpassword"]
                is_staff = data["is_staff"]
                is_superuser = data["is_superuser"]
                profile = data["profile"]
                gender = profile["gender"]
                security_group_id = data["security_group_id"]
                if not username:
                    return Response(
                        {"message": "Username is required", "success": False}
                    )
                elif _users.accountExists(request, lang):
                    return Response(
                        {
                            "message": "Username already exists, please choose another name",
                            "success": False,
                        }
                    )
                elif not first_name:
                    return Response(
                        {"message": "First name is required", "success": False}
                    )
                elif not last_name:
                    return Response(
                        {"message": "Last name is required", "success": False}
                    )
                elif password and len(password) < 6:
                    return Response(
                        {
                            "message": "Password is too short, must atleast 6 characters or above",
                            "success": False,
                        }
                    )
                elif password and not confirmpassword:
                    return Response(
                        {"message": "Please confirm your password", "success": False}
                    )
                elif password and not (confirmpassword == password):
                    return Response(
                        {"message": "Passwords don't match", "success": False}
                    )
                elif not gender:
                    return Response({"message": "Gender is required", "success": False})
                elif not security_group_id:
                    return Response(
                        {
                            "message": "Please select user's role",
                            "success": False,
                        }
                    )
                else:
                    user = _users.createAuthUser(request, lang, data)
                    return Response(user)
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False},
                    status=400,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


# Create Auth User
class UpdateAuthUserPassword(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, lang, userid):
        password = request.data["password"]
        confirmpassword = request.data["confirmpassword"]
        if not str(userid):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        if not password:
            return Response({"message": "Password is required", "success": False})
        elif not confirmpassword:
            return Response(
                {"message": "Confirmation password is also required", "success": False}
            )
        elif len(password) < 6:
            return Response(
                {
                    "message": "Password is too short, must atleast 6 characters or above",
                    "success": False,
                }
            )
        elif not confirmpassword:
            return Response(
                {"message": "Please confirm your password", "success": False}
            )
        elif not (confirmpassword == password):
            return Response({"message": "Passwords don't match", "success": False})
        else:
            user = _users.UpdateAuthUserPassword(request, lang, userid)
            return Response(
                {"message": "Password updated successfuly", "success": True},
                status=200,
            )


class UpdateAuthUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return Response(
            {
                "message": "Username already exists, please choose another name",
                "success": False,
            },
            status=400,
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
        if request.data:
            data = request.data
            if len(data) > 0:
                if (
                    "username" in data
                    or "email" in data
                    or "is_superuser" in data
                    or "security_group_id" in data
                    or "first_name" in data
                    or "last_name" in data
                    or "new_password" in data
                    or "confirm_password" in data
                    or "gender" in data
                    or "phoneno" in data
                    or "is_editable" in data
                    or "is_deletable" in data
                    or "bio" in data
                    or "address" in data
                    or "birth_date" in data
                    or "photo" in data
                    or "is_staff" in data
                    or "is_active" in data
                ):
                    if (
                        not data["username"]
                        and not data["email"]
                        and not str(data["is_superuser"])
                        and not str(data["security_group_id"])
                        and not data["first_name"]
                        and not data["last_name"]
                        and not str(data["profile_id"])
                        and not str(data["new_password"])
                        and not str(data["confirm_password"])
                        and not data["gender"]
                        and not str(data["phoneno"])
                        and not data["is_editable"]
                        and not data["is_deletable"]
                        and not data["bio"]
                        and not data["address"]
                        and not str(data["birth_date"])
                        and not data["photo"]
                        and not str(data["is_staff"])
                        and not str(data["is_active"])
                    ):
                        return Response(
                            {
                                "message": "Can't update when all fields are missing",
                                "success": False,
                            },
                            status=400,
                        )
                    else:
                        email = data["email"]
                        password = data["new_password"]
                        confirmpassword = data["confirm_password"]
                        if email and not _helper.isEmailValid(email):
                            return Response(
                                {"message": "Email is invalid", "success": False}
                            )
                        elif email and _users.emailExistsByUserId(
                            request, lang, userid, email
                        ):
                            return Response(
                                {"message": "Email already taken", "success": False}
                            )
                        elif password and len(password) < 6:
                            return Response(
                                {
                                    "message": "Password is too short, must atleast 6 characters or above",
                                    "success": False,
                                }
                            )
                        elif password and not confirmpassword:
                            return Response(
                                {
                                    "message": "Please confirm your password",
                                    "success": False,
                                }
                            )
                        elif password and not (confirmpassword == password):
                            return Response(
                                {"message": "Passwords don't match", "success": False}
                            )
                        else:
                            results = _users.UpdateAuthUser(request, lang, userid, data)
                            return Response(
                                {
                                    "message": "User updated successfuly",
                                    "success": True,
                                },
                                status=200,
                            )
            else:
                return Response(
                    {"message": "Incomplete data request", "success": False},
                    status=400,
                )
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


class getAllEmployeeTypes(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        results = _users.getAllEmployeeTypes(request, lang)
        return Response(results)


class GetEmployeeTypeById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, typeid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getEmployeeTypeById(request, lang, typeid)
        return Response(user)


class getAllEmployeeCategories(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        results = _users.getAllEmployeeCategories(request, lang)
        return Response(results)


class GetEmployeeCategoryById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, catid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getEmployeeCategoryById(request, lang, catid)
        return Response(user)


class GetAllClockModes(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getAllClockInOutModes(request, lang)
        return Response(user)


class GetClockModeById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, clockmodeid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getClockInOutModeById(request, lang, clockmodeid)
        return Response(user)


class getAllUsersClockTimeSettings(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getAllUsersClockTimeSettings(request, lang)
        return Response(user)


class getUsersClockTimeSettingById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, settingid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getUsersClockTimeSettingById(request, lang, settingid)
        return Response(user)


class getUsersClockTimeSettingByUserId(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getUsersClockTimeSettingByUserId(request, lang, userid)
        return Response(user)


class CreateUserClockTimeSetting(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if (
                "user" in data
                or "clockin_time" in data
                or "clockout_time" in data
                or "clockout_time" in data
                or "end_amplitude" in data
            ):
                if (
                    not data["user"]
                    and not data["clockin_time"]
                    and not str(data["is_superuser"])
                    and not str(data["start_amplitude"])
                    and not data["end_amplitude"]
                ):
                    return Response(
                        {
                            "message": "Can't update when all fields are missing",
                            "success": False,
                        },
                        status=400,
                    )
                else:
                    results = _users.createUserClockTimeSetting(request, lang, data)
                    return Response(results, status=200)
            return Response(results, status=200)
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )


# ClockIn
class ClockinUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        if "clockmode" not in request.data or "passkey" not in request.data:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        clockmode = request.data["clockmode"]
        passkey = request.data["passkey"]
        if not str(clockmode):
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        elif not str(passkey):
            return Response(
                {"message": "Password is required", "success": False}, status=400
            )
        else:
            # get user id
            userid = Token.objects.get(key=request.auth).user_id
            results = _users.ClockinUser(request, lang, clockmode, passkey, userid)
            if results["success"]:
                return Response(results)
            else:
                return Response(results, status=400)


# ClockOutUser
class ClockOutUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        # get user id
        results = _users.ClockOutUser(request, lang, userid)
        if results["success"]:
            return Response(results)
        else:
            return Response(results, status=400)


class GetAllClockInOutHistory(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        page = (
            1
            if "page" not in request.GET or not str(request.GET["page"])
            else int(request.GET["page"])
        )
        perpage = (
            25
            if "perpage" not in request.GET or not str(request.GET["perpage"])
            else int(request.GET["perpage"])
        )
        userid = (
            ""
            if "userid" not in request.GET or not str(request.GET["userid"])
            else int(request.GET["userid"])
        )
        is_cancelled = (
            False
            if "is_cancelled" not in request.GET or not str(request.GET["is_cancelled"])
            else (True if (is_cancelled == "true") else False)
        )
        has_clockedout = (
            ""
            if "has_clockedout" not in request.GET
            or not str(request.GET["has_clockedout"])
            else (True if (is_cancelled == "true") else False)
        )
        has_clockedin = (
            ""
            if "has_clockedin" not in request.GET
            or not str(request.GET["has_clockedin"])
            else (True if (is_cancelled == "true") else False)
        )
        # Date range
        dfrom = (
            ""
            if "from" not in request.GET or not str(request.GET["from"])
            else request.GET["from"]
        )
        dto = (
            ""
            if "from" not in request.GET or not str(request.GET["to"])
            else request.GET["to"]
        )
        results = _users.getAllClockOutInHistory(
            request,
            lang,
            userid,
            is_cancelled,
            page,
            perpage,
            dfrom,
            dto,
            has_clockedout,
            has_clockedin,
        )
        return Response(results)


class getUsersUnclockOutHistory(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.getUnClockedOutStatus(request, lang, userid)
        return Response(user)


class ResetClockOutToday(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        user = _users.ResetClockOutToday(request, lang, userid)
        return Response(user)


class ManuallyClockOutUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, clockinoutid):
        lang = DEFAULT_LANG if lang == None else lang
        if "clockout_time" not in request.GET:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
        elif not request.GET["clockout_time"]:
            return Response(
                {"message": "Please specify clockout time", "success": False},
                status=400,
            )
        results = _users.ManuallyClockOutUser(
            request, lang, clockinoutid, request.GET["clockout_time"]
        )
        #########################################
        if results["success"]:
            return Response(results)
        else:
            return Response(results, status=400)


class GetClockInOutById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, clockinoutid):
        lang = DEFAULT_LANG if lang == None else lang
        results = _users.GetClockInOutById(request, lang, clockinoutid)
        return Response(results)


class UpdateClockInOut(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # Request
    def post(self, request, lang, clockinoutid):
        lang = DEFAULT_LANG if lang == None else lang
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if (
                "user" in data
                or "clockin_time" in data
                or "clockout_time" in data
                or "has_clockin" in data
                or "has_clockout" in data
                or "mode_clockin" in data
                or "clockedout_by" in data
                or "clock_date" in data
                or "clockout_date" in data
                or "is_cancelled" in data
            ):
                if (
                    not data["user"]
                    and not data["clockin_time"]
                    and not str(data["is_superuser"])
                    and not str(data["start_amplitude"])
                    and not data["end_amplitude"]
                    and not data["user"]
                    and not data["clockin_time"]
                    and not str(data["is_superuser"])
                    and not str(data["start_amplitude"])
                    and not data["end_amplitude"]
                ):
                    return Response(
                        {
                            "message": "Can't update when all fields are missing",
                            "success": False,
                        },
                        status=400,
                    )
                else:
                    # results = _users.createUserClockTimeSetting(request, lang, data)
                    return Response({}, status=200)
            return Response({}, status=200)
        else:
            return Response(
                {"message": "Incomplete data request", "success": False}, status=400
            )
