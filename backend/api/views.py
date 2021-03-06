from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status, parsers, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from .models import Record, User
from .serializers import RecordSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from .permissions import IsAdminOrManager
# Create your views here.
class RecordViewSet(viewsets.ModelViewSet):
	queryset = Record.objects.all().order_by('-date_recorded')
	permission_classes = [IsAuthenticated,]
	serializer_class = RecordSerializer
	
	def perform_create(self, serializer):
		serializer.save()

	def perform_update(self, serializer):
		serializer.save()

	def get_queryset(self):
		qs = super(RecordViewSet, self).get_queryset()
		print("query_params.get data:", self.request.query_params)
		print("all querys: ", qs)
		date_from = self.request.query_params.get('from', None)
		date_to = self.request.query_params.get('to', None)
		if date_from is not None:
			qs = qs.filter(date_recorded__gte=date_from)
		if date_to is not None:
			qs = qs.filter(date_recorded__lte=date_to)
		print("selectred querys: ")
		return qs.filter_by_user(self.request.user)

class LoginView(APIView):
	authentication_classes = ()
	permission_classes = ()
	def post(self, request, format=None):
		email = request.data.get('email', '')
		password = request.data.get('password', '')
		user = authenticate(email=email, password=password)
		if user is not None:
			return Response("<html>Sign In Success!</html>", status=200)
		else:
			return Response("<html>Sign In Failure!</html>", status=401)	


class RegisterView(CreateModelMixin, GenericAPIView):
	serializer_class = UserCreateSerializer
	authentication_classes = ()

	def post(self, request):
		return self.create(request)

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	permission_classes = [IsAdminOrManager,]
	def get_serializer_class(self):
		if self.request.method in ['POST']:
			return UserCreateSerializer
		elif self.request.method in ['PUT', 'PATCH']:
			return UserUpdateSerializer
		else:
			return UserSerializer
	
	def get_queryset(self):
		qs = super(UserViewSet, self).get_queryset()
		return qs.filter_by_user(self.request.user)
	
	@action(detail=False, methods=['put', 'get'], permission_classes=[IsAuthenticated,], url_path='profile')
	def profile(self, request, *args, **kwargs):
		SerializerClass = self.get_serializer_class()
		if request.method in ['PUT']:
			serializer = SerializerClass(instance=request.user, data=request.data, context={'request': 'request'})
			serializer.is_valid(raise_exception=True)
			serializer.save()
		else:
			serializer = SerializerClass(instance=request.user)
		return Response(serializer.data)
	
	@action(detail=True, methods=['get'], permission_classes=[IsAuthenticated,], url_path='report')
	def report(self, request, *args, **kwargs):
		user = self.get_object()
		date_from = self.request.query_params.get('from', None)
		date_to = self.request.query_params.get('to', None)
		return Response(user.get_report(date_from=date_from, date_to=date_to))