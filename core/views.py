import requests
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.filters import ProfileFilter
from core.models import Profile
from core.serializers import UserSerializer, GroupSerializer, ProfileSerializer, UploadPhotoSerializer, \
    CreateOfferSerializer

import urllib
import json


class CurrentUser(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProfileViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter
    queryset = Profile.objects.all().order_by('-user__date_joined')

    def get_serializer_class(self):
        if self.action == 'set_photo':
            return UploadPhotoSerializer
        return ProfileSerializer

    def get_queryset(self):
        if self.action == 'search':
            return Profile.objects.filter(~Q(user__id=self.request.user.id)).order_by('-user__date_joined')

        return Profile.objects.all().order_by('-user__date_joined')


    @action(detail=True, methods=['put'])
    def set_photo(self, request, pk):
        serializer = self.get_serializer_class()(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = []

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        username = res.data['username']
        user = User.objects.get(username=username)
        user_group = Group.objects.get(name='user')
        user_group.user_set.add(user)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class PointsList(APIView):
    def get(self, request):
        url = 'https://b2b.taxi.tst.yandex.net/api/b2b/platform/pickup-points/list'
        headers = { 'Content-Type': 'application/json'}
        r = requests.post(url, headers=headers)

        return Response(r.json())

class ConfirmOffer(CreateAPIView):
    def post(self, request, *args, **kwargs):
        url = 'https://b2b.taxi.tst.yandex.net/api/b2b/platform/offers/confirm'
        headers = { 'Content-Type': 'application/json'}
        ser = CreateOfferSerializer(data=request.data)
        if ser.is_valid():
            print(ser.data)
            r = requests.post(url, data=ser.data, headers=headers)
            return Response(r.json())
        return Response(exception=True, status=400)