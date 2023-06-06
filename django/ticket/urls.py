
from django.urls import path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('tickets', TicketView)

urlpatterns = [
]
urlpatterns += router.urls
