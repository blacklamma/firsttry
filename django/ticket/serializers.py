
from .models import *
from rest_framework import serializers


class TicketListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tickets
        fields = ('id', 'display_id', 'summary')
