from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('login/', csrf_exempt(views.loginPage), name="login"),
    path('logout/', csrf_exempt(views.logoutPage), name="logout"),
]
