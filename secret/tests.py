from django.test import TestCase
from django.utils.crypto import get_random_string
from .models import Secret
from .serializers import SecretSerializer

class UserTest(TestCase):

    valid_secret_text = "my super secret"
    invalid_secret_text_1 = "0" * 1025
    invalid_secret_text_2 = ""
    invalid_secret_text_error_1 = "Ensure this field has no more than 1024 characters."
    invalid_secret_text_error_2 = "This field may not be blank."

    valid_expire_after = 1
    invalid_expire_after_1 = 0
    invalid_expire_after_2 = 4294967295
    invalid_expire_after_error_1 = "Ensure this value is greater than or equal to 1."
    invalid_expire_after_error_2 = "Ensure this value is less than or equal to 4294967294."

    valid_expire_after_views = 1
    invalid_expire_after_views_1 = 0
    invalid_expire_after_views_2 = 4294967295
    invalid_expire_after_views_error_1 = "Ensure this value is greater than or equal to 1."
    invalid_expire_after_views_error_2 = "Ensure this value is less than or equal to 4294967294."

    def test_create_valid_secret(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertTrue(serializer.is_valid())
        # print('!'*12)
        # print(serializer.errors)
        self.assertEqual(len(serializer.errors), 0)


    def test_create_invalid_secret_secretText_1(self):
        serializer = SecretSerializer(data= {
            'secretText': self.invalid_secret_text_1,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.get('secretText')[0],
            self.invalid_secret_text_error_1
            )

    def test_create_invalid_secret_secretText_2(self):
        serializer = SecretSerializer(data= {
            'secretText': self.invalid_secret_text_2,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.get('secretText')[0],
            self.invalid_secret_text_error_2
            )

    def test_create_invalid_secret_expireAfter_1(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.invalid_expire_after_1,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.get('expireAfter')[0],
            self.invalid_expire_after_error_1
            )

    def test_create_invalid_secret_expireAfter_2(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.invalid_expire_after_2,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.get('expireAfter')[0],
            self.invalid_expire_after_error_2
            )

    def test_create_invalid_secret_expireAfterViews_1(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.invalid_expire_after_views_1
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.get('expireAfterViews')[0],
            self.invalid_expire_after_views_error_1
            )

    def test_create_invalid_secret_expireAfterViews_2(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.invalid_expire_after_views_2
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.get('expireAfterViews')[0],
            self.invalid_expire_after_views_error_2
            )

    def test_get_exist_secret(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertTrue(serializer.is_valid())
        serializer.save()
        uuid = serializer.data.get('hash')
        secret = Secret.getDataByHash(uuid)
        self.assertEqual(secret['secretText'], self.valid_secret_text)
        self.assertEqual(secret['expireAfter'], self.valid_expire_after)
        self.assertEqual(secret['expireAfterViews'], self.valid_expire_after_views - 1)
        self.assertEqual(secret['hash'], uuid)


    def test_get_exist_secret_after_expire_views(self):
        serializer = SecretSerializer(data= {
            'secretText': self.valid_secret_text,
            'expireAfter': self.valid_expire_after,
            'expireAfterViews': self.valid_expire_after_views
        })
        self.assertTrue(serializer.is_valid())
        serializer.save()
        uuid = serializer.data.get('hash')
        Secret.getDataByHash(uuid)
        try:
            Secret.getDataByHash(uuid)
        except Exception as e:
            self.assertEqual(e.status_code, 404)

    def test_get_exist_secret_after_expire_time(self):
        token = Secret._encode_token(
            self.valid_secret_text,
            0,  # 0 minutes life
            self.valid_expire_after_views
        )
        uuid = get_random_string(32)
        secret = Secret.objects.create(
            data= token,
            uuid= uuid
        )
        secret.save()
        try:
            Secret.getDataByHash(uuid)
        except Exception as e:
            self.assertEqual(e.status_code, 404)
