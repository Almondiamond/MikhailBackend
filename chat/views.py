from django.db.models import Q
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat.models import Chat
from chat.serializers import ChatCreateSerializer, ChatListSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatCreateSerializer

        return ChatListSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(created_by__user=user) | Q(participant__user=user)).distinct()