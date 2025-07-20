from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

if TYPE_CHECKING:
    from django.db.models import Manager
    from django.db.models.options import Options

User = get_user_model()


class Person(models.Model):
    # Type annotations for Django
    objects: Manager[Person]
    _meta: Options[Person]

    # Gender Identity - self-identified
    GENDER_CHOICES = [
        ("woman", "Woman"),
        ("man", "Man"),
        ("non_binary", "Non-binary"),
        ("genderfluid", "Genderfluid"),
        ("agender", "Agender"),
        ("questioning", "Questioning"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    # Biological Sex - assigned at birth
    SEX_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("intersex", "Intersex"),
        ("unknown", "Unknown"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    # Pronouns
    PRONOUN_CHOICES = [
        ("she_her", "She/Her"),
        ("he_him", "He/Him"),
        ("they_them", "They/Them"),
        ("xe_xir", "Xe/Xir"),
        ("ze_zir", "Ze/Zir"),
        ("other", "Other"),
        ("ask_me", "Ask me"),
    ]

    # Inclusive naming fields
    full_name = models.CharField(
        max_length=200, help_text="Complete name as preferred by the person"
    )

    given_names = models.CharField(
        max_length=150,
        blank=True,
        help_text="Given/first names (space-separated if multiple)",
    )

    family_names = models.CharField(
        max_length=150,
        blank=True,
        help_text="Family/surname(s) (space-separated if multiple)",
    )

    preferred_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name to use in conversation (nickname, chosen name, etc.)",
    )

    # Optional: For cultures with patronymic/matronymic naming
    patronymic = models.CharField(
        max_length=100,
        blank=True,
        help_text="Patronymic name (father's name derivative)",
    )

    matronymic = models.CharField(
        max_length=100,
        blank=True,
        help_text="Matronymic name (mother's name derivative)",
    )

    # Optional: Additional name components
    middle_names = models.CharField(
        max_length=150,
        blank=True,
        help_text="Middle names (space-separated if multiple)",
    )

    suffix = models.CharField(
        max_length=20, blank=True, help_text="Name suffix (Jr., Sr., III, etc.)"
    )

    prefix = models.CharField(
        max_length=20, blank=True, help_text="Name prefix (Dr., Prof., etc.)"
    )

    # Legal name for official documents
    legal_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Full legal name as it appears on government documents",
    )

    date_of_birth = models.DateField(null=True, blank=True)

    # Gender and sex fields
    gender_identity = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        help_text="Self-identified gender",
    )

    biological_sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        blank=True,
        help_text="Sex assigned at birth",
    )

    pronouns = models.CharField(
        max_length=15,
        choices=PRONOUN_CHOICES,
        blank=True,
        help_text="Preferred pronouns for the person (e.g., 'she/her', 'he/him', 'they/them')",
    )

    custom_pronouns = models.CharField(
        max_length=50, blank=True, help_text="Custom pronouns (e.g., 'fae/faer')"
    )

    legal_sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        blank=True,
        help_text="Sex marker on legal documents",
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="persons_created",
        help_text="User who created this record",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="persons_updated",
        help_text="User who last updated this record",
    )

    class Meta:
        db_table = "person"

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        # Get the current user from the request if available
        user = kwargs.pop("user", None)

        if user:
            if not self.pk:  # New record
                self.created_by = user
            self.updated_by = user

        super().save(*args, **kwargs)

    @property
    def display_name(self):
        """Return the most appropriate name for display."""
        if self.preferred_name:
            return self.preferred_name
        if self.full_name:
            return self.full_name

        # Fallback construction
        name_parts = []
        if self.given_names:
            name_parts.append(self.given_names)
        if self.family_names:
            name_parts.append(self.family_names)

        return " ".join(name_parts) if name_parts else "Unknown"

    @property
    def formal_name(self):
        """Return formal name with prefix/suffix if available."""
        name = self.display_name
        if self.prefix:
            name = f"{self.prefix} {name}"
        if self.suffix:
            name = f"{name} {self.suffix}"
        return name

    @property
    def display_pronouns(self):
        """Return formatted pronouns for display."""
        if self.pronouns == "other" and self.custom_pronouns:
            return self.custom_pronouns
        return dict(self.PRONOUN_CHOICES).get(self.pronouns, "")

    def get_name_for_sorting(self):
        """Return name formatted for alphabetical sorting."""
        # Prefer family name for sorting, fall back to full name
        if self.family_names:
            return f"{self.family_names}, {self.given_names}".strip(", ")
        return self.full_name or self.display_name
