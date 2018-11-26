from rest_framework import serializers

from .models import Secret
from .constants import Constants as C

class SecretSerializer(serializers.Serializer):
    secretText = serializers.CharField(
        required= True,
        max_length= 1024,
        min_length= 1
        )
    expireAfter = serializers.IntegerField(
        required= True,
        min_value= C.MIN_INT32_VALUE,
        max_value = C.MAX_INT32_VALUE,
        )
    expireAfterViews = serializers.IntegerField(
        required= True,
        min_value= C.MIN_INT32_VALUE,
        max_value = C.MAX_INT32_VALUE,
        )
    hash = serializers.CharField(required= False)
    createdAt = serializers.CharField(required= False)

    def create(self, validated_data):
        secret = Secret.create(**validated_data)
        validated_data.update({
            'hash': secret.uuid,
            'createdAt': secret.created_at_str
        })
        return validated_data