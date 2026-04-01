from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    UserViewSet, RecordViewSet, DashboardView,
    login_page, dashboard_page, records_page, users_page
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'records', RecordViewSet, basename='record')

urlpatterns = [
    # HTML pages
    path('', login_page),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('records/', records_page, name='records'),
    path('users/', users_page, name='users'),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardView.as_view(), name='api_dashboard'),

    # auto generated swagger docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
]
