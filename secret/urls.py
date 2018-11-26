from django.urls import path
from .views import SecretCreateAPIView, SecretGetAPIView

urlpatterns = [
    path('', SecretCreateAPIView.as_view()),
    path('<uuid>', SecretGetAPIView.as_view())
]