from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "preferred_name",
        "display_name",
        "formal_name",
        "created_by",
        "updated_by",
    )
    search_fields = (
        "full_name",
        "preferred_name",
        "given_names",
        "family_names",
        "display_name",
    )
    list_filter = ("created_at", "updated_at", "created_by", "updated_by")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "preferred_name",
                    "given_names",
                    "family_names",
                    "prefix",
                    "suffix",
                    "pronouns",
                    "custom_pronouns",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )
