from django.shortcuts import render, HttpResponse

# from API_VERSIONS.default.Modules.Modules import  SystemModules
from .Modules import SystemModules
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

DEFAULT_LANG = "en"

# init module class
_modules = SystemModules()


def index(request):
    return HttpResponse("<h2>Invalid Entry point </h2>")


# Get all modules
class getAllModules(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _modules.getAllModules(request, lang)
        return JsonResponse(results, status=200, safe=False)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return JsonResponse(
            {"message": "Invalid request method", "status": "failed"}, status=400
        )


# Get main modules
class getMainModules(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _modules.getMainModules(request, lang)
        return JsonResponse(results, status=200, safe=False)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return JsonResponse(
            {"message": "Invalid request method", "status": "failed"}, status=400
        )


# Get all modules by id
class getModuleById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang, moduleid):
        lang = DEFAULT_LANG if lang == None else lang
        # if the moduleid is not given
        if not moduleid:
            return JsonResponse(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        # get module
        results = _modules.getModuleById(request, lang, moduleid)
        if not (results == None):
            # if there is results
            return JsonResponse(results, status=200, safe=False)
        else:
            # if there is no results
            return JsonResponse(
                {"message": "No record that matched this creteria", "status": "failed"},
                status=400,
            )

    def post(self, request, lang, moduleid):
        # invalid request method
        if not moduleid:
            return JsonResponse(
                {"message": "Invalid entry point", "status": "failed"}, status=400
            )
        lang = DEFAULT_LANG if lang == None else lang
        return JsonResponse(
            {"message": "Invalid request method", "status": "failed"}, status=400
        )


# Update modules
##:: Modules can be updated but only the display name and the rest is constant
class UpdateModule(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    ## GET MODULE ID
    def get(self, request, lang, moduleid):
        lang = DEFAULT_LANG if lang == None else lang
        # if the moduleid is not given
        if not moduleid:
            return JsonResponse(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        elif not ("module_name" in request.GET):
            return JsonResponse(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        elif not request.GET["module_name"]:
            return JsonResponse(
                {"message": "Module name is required", "status": "failed"}, status=400
            )
        else:
            # get module name
            module_name = request.GET["module_name"]
            # get module
            results = _modules.updateModuleName(request, lang, moduleid, module_name)
            if not (results == None):
                # if there is results
                return JsonResponse(results, status=200, safe=False)
            else:
                # if there is no results
                return JsonResponse(
                    {
                        "message": "No record that matched this creteria, zero records affected",
                        "status": "failed",
                    },
                    status=400,
                )
        # POSTS

    def post(self, request, lang, moduleid):
        # invalid request method
        lang = DEFAULT_LANG if lang == None else lang
        if not moduleid:
            return JsonResponse(
                {"message": "Invalid entry point", "status": "failed"}, status=400
            )
        else:
            return JsonResponse(
                {"message": "Invalid request method", "status": "failed"}, status=400
            )


# get sub modules
##:: Modules can be updated but only the display name and the rest is constant
class GetSubModules(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    ## GET MODULE ID
    def get(self, request, lang, moduleid):
        lang = DEFAULT_LANG if lang == None else lang
        # if the moduleid is not given
        if not moduleid:
            return JsonResponse(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        else:
            # get module
            results = _modules.getSubModules(request, lang, moduleid)
            if not (results == None):
                # if there is results
                return JsonResponse(results, status=200, safe=False)
            else:
                # if there is no results
                return JsonResponse(
                    {
                        "message": "No record that matched this creteria, zero records affected",
                        "status": "failed",
                    },
                    status=400,
                )
        # POSTS

    def post(self, request, lang, moduleid):
        # invalid request method
        lang = DEFAULT_LANG if lang == None else lang
        if not moduleid:
            return JsonResponse(
                {"message": "Invalid entry point", "status": "failed"}, status=400
            )
        else:
            return JsonResponse(
                {"message": "Invalid request method", "status": "failed"}, status=400
            )


# Disable module
##:: Modules can be updated but only the display name and the rest is constant
class DisableModules(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    ## GET MODULE ID
    def get(self, request, lang, moduleid):
        lang = DEFAULT_LANG if lang == None else lang
        # if the moduleid is not given
        if not moduleid:
            return JsonResponse(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        else:
            # get module
            results = _modules.disableModule(request, lang, moduleid)
            if not (results == None):
                # if there is results
                return JsonResponse(results, status=200, safe=False)
            else:
                # if there is no results
                return JsonResponse(
                    {
                        "message": "No record that matched this creteria, zero records affected",
                        "status": "failed",
                    },
                    status=400,
                )
        # POSTS

    def post(self, request, lang, moduleid):
        # invalid request method
        lang = DEFAULT_LANG if lang == None else lang
        if not moduleid:
            return JsonResponse(
                {"message": "Invalid entry point", "status": "failed"}, status=400
            )
        else:
            return JsonResponse(
                {"message": "Invalid request method", "status": "failed"}, status=400
            )


# Get Side menu modules
class getSideMenuModules(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        user_id = Token.objects.get(key=request.auth).user_id
        results = _modules.getSideBarModules(request, lang, user_id)
        return JsonResponse(results, status=200, safe=False)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return JsonResponse(
            {"message": "Invalid request method", "status": "failed"}, status=400
        )


# Get
class getDashboardMenu(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    # Request
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        results = _modules.getDashboardMenu(request, lang)
        return JsonResponse(results, status=200, safe=False)

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        return JsonResponse(
            {"message": "Invalid request method", "status": "failed"}, status=400
        )
