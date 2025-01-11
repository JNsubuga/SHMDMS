from .ReceivedDocuments import ReceivedDocuments
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.core.helper.helper import Helper

DEFAULT_LANG = "en"

#instantiate receivedDocument class
_receivedDocument = ReceivedDocuments()
_helper = Helper()

class getAllReceivedDocuments(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _receivedDocument.getAllReceivedDocuments(request, lang)
        return Response(response)
    
class getReceivedDocumentById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, receiveddocumentid):
        lang = DEFAULT_LANG if lang == None else lang
        if not receiveddocumentid:
            return Response(
                {
                    "message": "Incomplete data request!!!",
                    "status": False
                }, status=400
            )
        elif not _receivedDocument.ReceivedDocumentExists(receiveddocumentid):
            return Response(
                {
                    "message": "Document doesn't exist in the records!!!",
                    "status": False
                }, status=400
            )
        response = _receivedDocument.getReceivedDocumentById(request, lang, receiveddocumentid)
        return Response(response)
    
class registerReceivedDocument(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        data = request.data
        ##########################################
        token_auth = _helper.getAuthToken(request)
        if not token_auth["status"]:
            return Response(
                token_auth,
                status=400
            )
        token = token_auth["token"]
        ##########################################
        userid = Token.objects.get(key=token).user_id
        if len(data) > 0:
            if not data["memo"]:
                return Response(
                    {
                        "message": "Memo is a required field!!!",
                        "status": False
                    }
                )
            elif not data["officeFrom"]:
                return Response(
                    {
                        "message": "Leter From/Office is a required field!!!",
                        "status": False
                    }
                )
            elif not data["dateReceived"]:
                return Response(
                    {
                        "message": "Received At is a required field!!!",
                        "status": False
                    }
                )
            elif not data["contactNumber"]:
                return Response(
                    {
                        "message": "Contact Number is a required field!!!",
                        "status": False
                    }
                )
            else:
                _receivedDocument.registerReceivedDocument(userid, data)
                return Response(
                    {
                        "message": "Received Document is Registered Successfully!!",
                        "status": True
                    }, status=201
                )
                # return Response (_receivedDocument.registerReceivedDocument(userid, data))
        else:
            return Response(
                {
                    "message": "No data Submitted to the database!!!",
                    "status": False
                }, status=400
            )
        

class updateReceivedDocument(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def put(self, request, lang, receiveddocumentid):
        lang = DEFAULT_LANG if lang == None else lang
        if not int(receiveddocumentid):
            return Response(
                {
                    "message": "Incomplete data request!!!",
                    "status": False
                }, status=400
            )
        elif not _receivedDocument.ReceivedDocumentExists(receiveddocumentid):
            return Response(
                {
                    "message": "Document does not Exist in registered received records!!!",
                    "status": False
                }, status=400
            )
        else:
            data = request.data
            _receivedDocument.updateReceivedDocument(receiveddocumentid, data)
            return Response(
                {
                    "message": "Record Successfully Updated!!",
                    "status": True
                }, status=201
            )
        