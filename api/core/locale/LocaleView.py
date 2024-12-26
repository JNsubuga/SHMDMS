from django.shortcuts import render

# Create your views here.
from .Locale import Locale
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.models import SecurityGroup, UserProfile, UserGroup, UserPermission
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

DEFAULT_LANG = "en"

# init locale class
_locale = Locale()


class DefaultCountry(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        content = _locale.getDefaultCountry(request, lang)
        return Response(content)


class UpdateDefaultCountry(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang
        if not ("countryid" in request.GET):
            return Response(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        elif not request.GET["countryid"]:
            return Response(
                {"message": "Incomplete is required", "status": "failed"}, status=400
            )
        else:
            countryid = request.GET["countryid"]
            _locale.UpdateDefaultCountry(request, lang, countryid)
            return Response(
                {"message": "Country updated succesfully", "status": "success"}
            )

# Regions
class getAllRegions(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _locale.getAllRegions(request, lang)
        return Response(response)


class getRegionById(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]

    def get(self, request, lang, regionid):
        lang = DEFAULT_LANG if lang == None else lang
        if not regionid:
            return Response(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        elif not _locale.RegionExists(request, lang, regionid):
            return Response(
                {"message": "Region doesn't exist", "status": "failed"}, status=400
            )
        ### response
        response = _locale.getRegionById(request, lang, regionid)
        return Response(response)

# District
class getAllDistricts(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]
    
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _locale.getAllDistricts(request, lang)
        return Response(response)
   
    
class getDistrictById(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]
    
    def get(self, request, lang, districtid):
        lang = DEFAULT_LANG if lang == None else lang
        if not districtid:
            return Response(
                {"message":"Incomplete data request", "status":"failed"}, status=400
            )
        elif not _locale.DistrictExists(request, lang, districtid):
            return Response(
                {"message": "District doesn't exist", "status": "failed"}, status=400
            )
        ### response
        response = _locale.getDistrictById(request, lang, districtid)
        return Response(response)
    
    
    
# Sub County
class getAllSubCounties(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]
    
    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _locale.getAllSubCounties(request, lang)
        return Response(response)
   
    
class getSubCountyById(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ["get"]
    
    def get(self, request, lang, subcountyid):
        lang = DEFAULT_LANG if lang == None else lang
        if not subcountyid:
            return Response(
                {"message":"Incomplete data request", "status":"failed"}, status=400
            )
        elif not _locale.SubCountyExists(request, lang, subcountyid):
            return Response(
                {"message": "District doesn't exist", "status": "failed"}, status=400
            )
        ### response
        response = _locale.getSubCountyById(request, lang, subcountyid)
        return Response(response)