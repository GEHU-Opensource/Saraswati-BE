from django.contrib import admin
from .models import Organisation, DepartmentAdmin


# Inline for Department Admins (Inside Organisation)
class DepartmentAdminInline(admin.TabularInline):
    model = DepartmentAdmin
    extra = 1
    fields = ("user", "role", "status")
    show_change_link = True  # Enables quick editing
    autocomplete_fields = ["user"]  # Enables search for users in Department Admins


# Organisation Model in Admin (With Department Admins)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "admin_name",
        "contact_email",
        "date_created",
        "status",
    )

    search_fields = ("name", "admin__username", "contact_email")
    list_filter = ("date_created",)
    inlines = [DepartmentAdminInline]  # Show Department Admins inside Organisation

    def admin_name(self, obj):
        return obj.admin.username if obj.admin else "No Admin Assigned"

    admin_name.short_description = "Organisation Admin"


# Department Admin Model in Django Admin
class DepartmentAdminConfig(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "status")
    search_fields = ("user__username", "organisation__name")
    list_filter = ("organisation",)


# Register models
admin.site.register(Organisation, OrganisationAdmin)

