from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from .serializers import TicketListSerializer
from .models import Tickets
from rest_framework import viewsets
from rest_framework.decorators import action


class TicketView(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            init_filter = Q(is_deleted=False)
            init_filter &= (Q(assignee_id=request.user.id) |
                            Q(created_by_id=request.user.id))
            ticket_obj = Tickets.objects.filter(init_filter)
            # Show 25 contacts per page.
            paginator = Paginator(ticket_obj, 25)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            serializer = TicketListSerializer(page_obj, many=True)
            ticket_data = serializer.data
            final_data = [dict(x) for x in ticket_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)
