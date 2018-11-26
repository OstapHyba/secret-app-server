from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.exceptions import NotFound
import jwt

from .helpers import is_expired
from .constants import Constants as C

jwt_settings = getattr(settings, 'JWT_SETTINGS')

class Secret(models.Model):
    uuid = models.CharField(
        max_length= 32,
        blank= False,
        null= False,
        editable= False
        )
    data = models.CharField(
        max_length= 1024,
        blank= False,
        null= False,
        )
    created_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name = 'Secret'
        verbose_name_plural = 'Secrets'

    @property
    def created_at_str(self):
        return self.created_at.ctime()

    @staticmethod
    def _encode_token(secretText, expireAfter, expireAfterViews):
        return jwt.encode(
            {
                'secretText': secretText,
                'expireAfter': expireAfter,
                'expireAfterViews': expireAfterViews,
            },
            jwt_settings['JWT_SECRET_KEY'],
            jwt_settings['JWT_ALGORITHM'],
        ).decode('utf-8')

    @staticmethod
    def _decode_token(token):
        return jwt.decode(
            token,
            jwt_settings['JWT_SECRET_KEY'],
            jwt_settings['JWT_VERIFY'],
            options= {
                'verify_exp': jwt_settings['JWT_VERIFY_EXPIRATION'],
            },
            leeway= jwt_settings['JWT_LEEWAY'],
            audience= jwt_settings['JWT_AUDIENCE'],
            issuer= jwt_settings['JWT_ISSUER'],
            algorithms= [jwt_settings['JWT_ALGORITHM']]
        )

    @classmethod
    def create(cls, secretText, expireAfter, expireAfterViews):
        encoded = cls._encode_token(secretText, expireAfter, expireAfterViews)
        return cls.objects.create(data= encoded, uuid= get_random_string(32))

    @classmethod
    def getDataByHash(cls, uuid):
        instance = cls.objects.filter(uuid= uuid).first()

        if not instance:
            raise NotFound
        
        payload = instance._decode_token(instance.data)
        created_at = instance.created_at_str

        if is_expired(instance.created_at, payload['expireAfter']):
            instance.delete()
            raise NotFound

        payload['expireAfterViews'] -= 1

        if payload['expireAfterViews'] == 0:
            instance.delete()
        else:
            instance.data = instance._encode_token(**payload)
            instance.save()
        
        payload['hash'] = uuid
        payload['createdAt'] = created_at

        return payload


