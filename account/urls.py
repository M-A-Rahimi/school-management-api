from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QueueSignUpViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'queue-signup', QueueSignUpViewSet, basename='queue-signup'),

urlpatterns = [    
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
    
