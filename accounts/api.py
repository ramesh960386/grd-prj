from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import AuthenticateSerializer, UserSerializer, VerifySerializer
from .models import User
from .email import *
import random, redis


rds = redis.StrictRedis(port=6379, db=0)

def generate_code(email):
    code = random.randint(100000, 999999)
    rds.set(email, code)
    return send_otp_via_email(email, code)


class SendCode(APIView):
    permission_classes = [AllowAny]

    def post(self, request):      
        try:
            email = request.data['email']
            if email:
                if True:
                    return Response({'status':200, 'message': 'code is successfully sent the your email'})
                return Response({'status': 400, 'message': 'something went wrong in email'})
            else:
                return Response({'status': 400, 'message': 'email field is empty'})
        except Exception as e:
            return Response({'status': 400, 'message': 'something went wrong'})


class VerifyCode(APIView):
    permission_classes = [AllowAny]    

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            req_code = str(request.data['code'])
            email_code = rds.get(email)
            if email_code:
                email_code = email_code.decode("utf-8")
                if email_code == req_code:
                    return Response({
                        "success": True, "code": 200,
                        "message":"email code is verified"}, status=status.HTTP_200_OK
                    )
                return Response({
                    "success": False, "code": 400,
                    "message":"wrong code"},status=status.HTTP_400_BAD_REQUEST
                )  
            return Response({
                "success": False, "code": 400,
                "message":"email does not exist or code is not generated"},
                status=status.HTTP_400_BAD_REQUEST
            )   
        return Response({
            "success": False, "code": 400, "data": serializer.errors,
            "message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                # send_otp_via_email(email, code)
                return Response({
                    'status': 200,
                    'message': 'your registration has been successfully completed',
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': 400,
                    'message': 'something went wrong',
                    'data': serializer.errors
                })
        except Exception as e:
            print(e)


class UserAuthenticate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthenticateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                "success": True, "code": 200,
                "message":"User is successfully Authenticated"}, status=status.HTTP_200_OK
            )
        return Response({
            "success": False, "code": 400, "data": serializer.errors,
            "message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserList(ListAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer