from django.urls import path, include
from rest_framework import routers
from myapp.views import MyUserViewSet, ProductViewSet, LoginApiView, LogoutApiView, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

router = routers.SimpleRouter()
router.register('users', MyUserViewSet, basename='users')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginApiView.as_view(), name='login'),
    path('logout', LogoutApiView.as_view(), name='logout'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
