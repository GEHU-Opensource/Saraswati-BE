from django.urls import path
from .views import *

urlpatterns = [
    path("exam/create/", create_exam, name="create_exam"),
]
