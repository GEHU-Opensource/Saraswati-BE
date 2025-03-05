from rest_framework import serializers
from user_app.models import AppUser


class get_users_csv_serializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["student_name", "university_email", "university_id", "marks"]


class upload_users_csv_serializer(serializers.Serializer):
    file = serializers.FileField()
