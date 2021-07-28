from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer(many=True)
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
