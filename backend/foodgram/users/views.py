from rest_framework.permissions import AllowAny

from djoser.views import UserViewSet

from .models import User
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer(many=True)
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
