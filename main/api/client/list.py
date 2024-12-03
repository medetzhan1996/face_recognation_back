from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from main.models import Client



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
