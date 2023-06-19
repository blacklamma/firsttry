from django.urls import path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('emails', EmailView)
router.register('wf', WorkflowView)
router.register('status', StatusView)
router.register('rule', RuleView)
router.register('notif', NotifView)


urlpatterns = [
]

urlpatterns += router.urls
