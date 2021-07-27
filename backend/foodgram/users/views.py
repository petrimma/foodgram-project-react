from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters, mixins, status, viewsets

from django.shortcuts import get_object_or_404


from .serializers import CustomUserSerializer 
from .models import User


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer(many=True)
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
