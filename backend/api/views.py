from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status, parsers, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
# from rest_framework_jwt.utils import jwt_response_payload_handler
from django.http import JsonResponse
from .models import Entry, User
from .serializers import EntrySerializer, UserSerializer, UserCreateSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
# Create your views here.
class EntryViewSet(viewsets.ModelViewSet):
	queryset = Entry.objects.all()
	serializer_class = EntrySerializer

class LoginView(APIView):
	authentication_classes = ()
	permission_classes = ()
	def post(self, request, format=None):
		email = request.data.get('email', '')
		password = request.data.get('password', '')
		user = authenticate(email=email, password=password)

		print (user)

		if user is not None:
			return Response("<html>Sign In Success!</html>", status=200)
		else:
			return Response("<html>Sign In Failure!</html>", status=401)	


class RegisterView(CreateModelMixin, GenericAPIView):
	serializer_class = UserCreateSerializer
	authentication_classes = ()

	def post(self, request):
		return self.create(request)

