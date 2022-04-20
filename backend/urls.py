"""myprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts import api
from oauth2_provider import views as o2v
# from oauth2_provider.urls

schema_view = get_schema_view(
    openapi.Info(
        title="WAL API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="test@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    # authentication_classes=(authentication.TokenAuthentication),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login_token/', o2v.TokenView.as_view(), name='login-token'),
    path('api/refresh_token/', o2v.TokenView.as_view(), name='refresh-token'),
    path('api/logout_token/', o2v.RevokeTokenView.as_view(), name='logout-token'),
    path('api/accounts/', include('accounts.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]