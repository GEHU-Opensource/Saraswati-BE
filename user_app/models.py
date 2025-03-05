from django.db import models

class AppUser(models.Model):
    USER_TYPES = [
        ("registered_user", "Registered User"),
        ("guest_user", "Guest User"),
    ]
    user_id = models.BigAutoField(primary_key=True)
    university_id = models.BigIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=50, choices=USER_TYPES, null=True, blank=True
    )
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    semester = models.IntegerField()
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, unique=True)
    cdate = models.DateTimeField(auto_now_add=True)
    valid_till = models.DateTimeField(null=True, blank=True)
    last_logged_in = models.DateTimeField(null=True, blank=True)
    auth_token = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    ) 
    reset_count = models.PositiveIntegerField(
        default=0
    )
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} ({self.university_id or 'N/A'})"