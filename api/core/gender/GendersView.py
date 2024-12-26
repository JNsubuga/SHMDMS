# Create your views here
from .Genders import Genders
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

DEFAULT_LANG = "en"

# init Gender class
_gender = Genders()


class getAllGenders(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _gender.getAllGenders(request, lang)
        return Response(response)


class getGenderById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, genderid):
        lang = DEFAULT_LANG if lang == None else lang
        if not genderid:
            return Response(
                {"message": "Incomplete data request", "status": "failed"}, status=400
            )
        elif not _gender.GenderExists(request, lang, genderid):
            return Response(
                {"massage": "Gender doesn't Exist", "status": "failed"}, status=400
            )
        # response
        response = _gender.getGenderById(request, lang, genderid)
        return Response(response)


class createGender(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        data = request.data
        if len(data) > 0:
            if not data["gender_name"]:
                return Response(
                    {"message": "gender_name Field is required!!!", "status": False},
                    status=403,
                )
            elif not data["initials"]:
                return Response(
                    {"message": "The initials Field is required!!!", "status": False},
                    status=403,
                )
            elif not data["is_disabled"]:
                return Response(
                    {"message": "Gender Status Failed is required!!!", "status": False},
                    status=403,
                )
            else:
                _gender.createGender(request, lang, data)
                return Response(
                    {"message": "Gender Successfully Saved!!", "status": True},
                    status=201,
                )
        else:
            return Response(
                {"message": "No data submited to the database!!!", "status": False},
                status=403,
            )


class updateGender(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def put(self, request, lang, genderid):
        lang = DEFAULT_LANG if lang == None else lang
        if not int(genderid):
            return Response(
                {"message": "Incomplete data request!!!", "status": "Failed"},
                status=400,
            )
        if not _gender.GenderExists(request, lang, genderid):
            return Response(
                {"message": "Gender doesn't Exist!!!", "status": "Failed"}, status=400
            )
        else:
            data = request.data
            _gender.updateGender(data, genderid)
            return Response(
                {"message": "Gender Successfully Updated!!", "status": True}, status=202
            )
