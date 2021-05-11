from speaker_verification.models import User
from rest_framework.serializers import ModelSerializer, CharField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'embedding')

