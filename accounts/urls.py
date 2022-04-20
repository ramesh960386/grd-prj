from django.urls import path
from accounts import api

urlpatterns = [
    path('send_code/', api.SendCode.as_view()),
    path('verify_code/', api.VerifyCode.as_view()),
    path('signup/', api.RegisterAPIView.as_view()),
    path('user_authenticate/', api.UserAuthenticate.as_view()),
    path('users/', api.UserList.as_view()),
    path('users/<pk>/', api.UserDetails.as_view()),
]