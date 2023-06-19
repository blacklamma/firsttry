from django.urls import path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('users', UserView)
router.register('customers', CustomerView)
router.register('role', RoleView)


urlpatterns = [
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
]

urlpatterns += router.urls
