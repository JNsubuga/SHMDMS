# All Things related to modules
from datetime import datetime
from locale import currency
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from pytz import country_names
from api.core.helper import helper, webconfig
from api.models import *
from django.db.models import Count
from django.db.models import Q

# helper class
# master module class
from yaml import load, dump
import json
from django.core.serializers.json import DjangoJSONEncoder

###############

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from django.core import serializers


# master module class
class Locale:
    def __init__(self):
        self.help = helper.Helper()
        
    # Districts
    def getAllDistricts(self, request, lang):
        results = []
        districts = District.objects.filter(is_disabled=False).order_by("-id")
        for district in districts:
            district_item = {
                "id": district.pk,
                "district_name": district.district_name,
                "code_name": district.code_name,
                "is_disabled": district.is_disabled,
                "created": district.created
            }
            results.append(district_item)
        return results
    
    def DistrictExists(self, request, districtid):
        return District.objects.filter(pk=int(districtid)).exists()
    
    def getDistrictById(self, request, districtid):
        district = District.objects.filter(pk=int(districtid)).get()
        return {
            "id": district.pk,
            "district_name": district.district_name,
            "code_name": district.code_name,
            "is_disabled": district.is_disabled,
            "created": district.created
        }