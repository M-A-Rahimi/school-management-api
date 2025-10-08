from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import QueueSignUpSerializer
from .models import QueueSignUp
from .permission import IsSuperUser
class QueueSignUpViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing QueueSignUp records.

    Permissions:
        - Anyone can create a new record (POST /queue-signups/)
        - Only superusers can list, retrieve, update, or delete records

    Features:
        - Supports filtering by `status` via query parameters, e.g.:
            /queue-signups/?status=p  -> pending
            /queue-signups/?status=a  -> accepted
            /queue-signups/?status=r  -> rejected
        - Uses the default project pagination for list responses
        - Full CRUD support
    """
    serializer_class = QueueSignUpSerializer
    queryset = QueueSignUp.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        else:
            return [IsSuperUser()]        
        

class LoginView(APIView):
    """
        Handles user login and JWT token generation.

        Permissions:
            - Allow any user to access (no authentication required).

        Functionality:
            - Accepts POST requests with 'username' and 'password'.
            - Authenticates the user using Django's authenticate().
            - If successful:
                - Generates JWT access and refresh tokens.
                - Returns tokens in JSON response.
                - Sets tokens as HttpOnly cookies for secure client storage.
            - If authentication fails:
                - Returns 401 with an error message.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
            # Set secure cookies
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, samesite='Lax',)
            response.set_cookie('refresh_token', str(refresh), httponly=True, samesite='Lax',)
            return response

        return Response({'error': 'Invalid credentials'}, status=401)


class LogoutView(APIView):
    """
        Handles user logout and refresh token blacklisting.

        Permissions:
            - Requires user to provide a valid refresh token.

        Functionality:
            - Accepts POST requests with 'refresh_token' in the body (or can be read from cookie).
            - Blacklists the provided refresh token to prevent future use.
            - Deletes 'access_token' and 'refresh_token' cookies from the client.
            - Returns a confirmation message.
            - If refresh token is missing or invalid, returns an error response.
    """
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist() 
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Logged out"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response