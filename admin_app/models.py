from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


class Organisation(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit unique identifier
    name = models.CharField(max_length=100, unique=True)
    admin = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, related_name="org_admin"
    )  # Single admin

    ROLE_CHOICES = [
        ("ORG_ADMIN", "Organisation Admin"),
        ("ORG_EDITOR", "Organisation Editor"),
        ("ORG_VIEWER", "Organisation Viewer"),
    ]
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="ORG_ADMIN"
    )  # Single Role

    contact_email = models.EmailField(
        unique=True, null=True, blank=True
    )  # Contact email for the organisation
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Department Admins (Admins Assigned to Organisation)
class DepartmentAdmin(models.Model):
    ROLE_CHOICES = [
        ("DEPT_ADMIN", "Department Admin"),
        ("DEPT_EDITOR", "Department Editor"),
        ("DEPT_VIEWER", "Department Viewer"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dept_admins"
    )  # Delete user when admin is deleted
    organisation = models.ForeignKey(
        Organisation, on_delete=models.PROTECT, related_name="dept_admins"
    )  # Prevent deletion of Organisation
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.organisation.name} - {self.get_role_display()}"


# Signal to delete user when DepartmentAdmin is deleted
@receiver(post_delete, sender=DepartmentAdmin)
def delete_user_with_admin(sender, instance, **kwargs):
    """
    Deletes the associated User when a DepartmentAdmin is deleted.
    """
    if instance.user:
        instance.user.delete()


class admins(models.Model):
    ADMIN_TYPES = [
        ("organisation", "Organisation"),
        ("department", "Department"),
    ]
    admin_type = models.CharField(
        max_length=50, choices=ADMIN_TYPES, default="department"
    )
    user_id = models.BigAutoField(primary_key=True)
    created_for_department = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, unique=True)
    cdate = models.DateTimeField(auto_now_add=True)
    valid_till = models.DateTimeField(null=True, blank=True)
    last_logged_in = models.DateTimeField(null=True, blank=True)
    auth_token = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Hashes the password before saving"""
        if not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} ({self.admin_type})"
