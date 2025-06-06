from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat.models import Chat
from chat.serializers import ChatCreateSerializer, ChatListSerializer, ChatRetrieveSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatCreateSerializer

        if self.action == 'retrieve':
            return ChatRetrieveSerializer

        return ChatListSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(created_by__user=user) | Q(participant__user=user)).distinct()

    @action(methods=['post'], detail=True, url_path='messages')
    def send_message(self, request):
        return Response({ 'key': 'hellow-rodl!' })

    @action(methods=['patch'], detail=True, url_path=r'messages/(?P<message_id>\d+)')
    def edit_message(self, request):
        return Response({ 'key': 'hellow-rodl!' })
