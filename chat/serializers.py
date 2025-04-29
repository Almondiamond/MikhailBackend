from rest_framework import serializers

from chat.models import Chat
from core.models import Profile
from core.serializers import ProfileSerializer


class ChatListSerializer(serializers.ModelSerializer):
    participant = ProfileSerializer()
    created_by = ProfileSerializer()

    class Meta:
        model = Chat
        fields = '__all__'


class ChatRetrieveSerializer(serializers.ModelSerializer):
    participant = ProfileSerializer()
    created_by = ProfileSerializer()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'

    def get_messages(self, obj):
        return


class ChatCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    participant_username = serializers.CharField(write_only=True)

    class Meta:
        model = Chat
        fields = ['created_by', 'participant_username', 'approved', 'created_at']
        read_only_fields = ['created_at', 'created_by']  # Эти поля будут только для чтения

    def validate_participant_username(self, value):
        try:
            Profile.objects.get(user__username=value)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile with this username does not exist.")
        return value

    def create(self, validated_data):
        participant_username = validated_data.pop('participant_username')
        participant = Profile.objects.get(user__username=participant_username)
        print(self.data['created_by'])
        created_by = Profile.objects.get(user__username=self.data['created_by'])
        chat = Chat.objects.create(
            participant=participant,
            created_by=created_by
        )

        return chat
