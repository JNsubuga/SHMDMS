from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from rest_framework.authentication import (
    SessionAuthentication,
    BaseAuthentication,
    TokenAuthentication
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Create your views here
class index(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, format=None):
        return HttpResponse("<h2>Invalid entry point</h2>")
    
class GetUserView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, format=None):
        content = {
            "user": str(request.user), #`django.contrib.auth.User` instance.
            "auth": str(request.auth) # None
        }
        return Response(content)
    
# Generate custom AUTH TOken
class CreateUserAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key, 
                "user_id": user.pk, 
                "email":user.email
            }
        )