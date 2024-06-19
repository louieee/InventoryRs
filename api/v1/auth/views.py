from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.auth.serializer import LoginSerializer, ChangePasswordSerializer


class LoginView(APIView):
	http_method_names = ("post",)
	permission_classes = [AllowAny]

	@swagger_auto_schema(
		request_body=LoginSerializer,
		operation_summary="logs in an employee",
	)
	def post(self, request, *args, **kwargs):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		token = serializer.login()
		return Response(dict(token=token))


class ChangePasswordView(APIView):
	http_method_names = ("post",)
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		request_body=ChangePasswordSerializer,
		operation_summary="updates logged in employee's password",
	)
	def post(self, request, *args, **kwargs):
		serializer = ChangePasswordSerializer(data=request.data, instance=request.user)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(status=200)
