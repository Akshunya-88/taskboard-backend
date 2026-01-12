from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
