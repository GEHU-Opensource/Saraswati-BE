import csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from user_app.models import AppUser
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.decorators import api_view
from admin_app.serializers import (
    get_users_csv_serializer,
    upload_users_csv_serializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from admin_app.constants import *
from django.db import IntegrityError
from rest_framework import status
from django.shortcuts import render


def home(request):
    return render(request, "index.html")

    # university_id = models.BigIntegerField(unique=True)
    # name = models.CharField(max_length=255)
    # course = models.CharField(max_length=255)
    # branch = models.CharField(max_length=255)
    # semester = models.CharField(max_length=50)
    # email = models.EmailField(unique=True)
    # phone_no = models.BigIntegerField(unique=True)

@api_view(["GET"])
def get_users_csv(request):
    page_number = request.GET.get("page", 1)
    items_per_page = 100

    users = AppUser.objects.all()
    paginator = Paginator(users, items_per_page)
    page = paginator.get_page(page_number)

    serializer = get_users_csv_serializer(page.object_list, many=True)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    for user in serializer.data:
        writer.writerow(
            [
                user.get("name", ""),
                user.get("email", ""),
                user.get("university_id", ""),
                # user.get("marks", ""),
            ]
        )
    return response






