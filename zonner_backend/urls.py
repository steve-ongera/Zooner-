from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Zooner API",
      default_version='v1',
      description="API documentation for the Zooner platform (Django + React + Android)",
      terms_of_service="https://www.zooner.com/terms/",
      contact=openapi.Contact(email="support@zooner.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('zooner.urls')),  # your app-level routes
    
    # Swagger & ReDoc UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
