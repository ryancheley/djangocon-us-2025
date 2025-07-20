"""Tests for patient models."""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from patient.models import Person

User = get_user_model()


class PersonModelTest(TestCase):
    """Test cases for the Person model."""

    def setUp(self):
        """Set up test data."""
        test_password = "testpass123"  # noqa: S105
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password=test_password
        )

    def test_person_creation_minimal(self):
        """Test creating a Person with minimal required fields."""
        person = Person.objects.create(
            full_name="Jane Doe", created_by=self.user, updated_by=self.user
        )

        self.assertEqual(person.full_name, "Jane Doe")
        self.assertEqual(person.created_by, self.user)
        self.assertEqual(person.updated_by, self.user)
        self.assertIsNotNone(person.created_at)
        self.assertIsNotNone(person.updated_at)

    def test_person_creation_complete(self):
        """Test creating a Person with all fields populated."""
        person = Person.objects.create(
            full_name="Dr. Jane Elizabeth Doe Jr.",
            given_names="Jane Elizabeth",
            family_names="Doe",
            preferred_name="Jane",
            patronymic="Johnsdottir",
            matronymic="Marisdottir",
            middle_names="Elizabeth",
            suffix="Jr.",
            prefix="Dr.",
            legal_name="Jane Elizabeth Doe",
            gender_identity="woman",
            biological_sex="female",
            pronouns="she_her",
            legal_sex="female",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.full_name, "Dr. Jane Elizabeth Doe Jr.")
        self.assertEqual(person.given_names, "Jane Elizabeth")
        self.assertEqual(person.family_names, "Doe")
        self.assertEqual(person.preferred_name, "Jane")
        self.assertEqual(person.gender_identity, "woman")
        self.assertEqual(person.biological_sex, "female")
        self.assertEqual(person.pronouns, "she_her")

    def test_display_name_property_preferred(self):
        """Test display_name returns preferred_name when available."""
        person = Person.objects.create(
            full_name="Jonathan Smith",
            preferred_name="Jon",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.display_name, "Jon")

    def test_display_name_property_full_name(self):
        """Test display_name returns full_name when no preferred_name."""
        person = Person.objects.create(
            full_name="Jonathan Smith", created_by=self.user, updated_by=self.user
        )

        self.assertEqual(person.display_name, "Jonathan Smith")

    def test_display_name_property_fallback(self):
        """Test display_name fallback to given_names + family_names."""
        person = Person.objects.create(
            full_name="",
            given_names="Jonathan",
            family_names="Smith",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.display_name, "Jonathan Smith")

    def test_display_name_property_unknown(self):
        """Test display_name returns 'Unknown' when no names available."""
        person = Person.objects.create(
            full_name="", created_by=self.user, updated_by=self.user
        )

        self.assertEqual(person.display_name, "Unknown")

    def test_formal_name_property_with_prefix_suffix(self):
        """Test formal_name includes prefix and suffix."""
        person = Person.objects.create(
            full_name="Jane Doe",
            prefix="Dr.",
            suffix="Jr.",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.formal_name, "Dr. Jane Doe Jr.")

    def test_formal_name_property_no_prefix_suffix(self):
        """Test formal_name without prefix/suffix."""
        person = Person.objects.create(
            full_name="Jane Doe", created_by=self.user, updated_by=self.user
        )

        self.assertEqual(person.formal_name, "Jane Doe")

    def test_display_pronouns_property_standard(self):
        """Test display_pronouns for standard pronoun choices."""
        person = Person.objects.create(
            full_name="Jane Doe",
            pronouns="they_them",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.display_pronouns, "They/Them")

    def test_display_pronouns_property_custom(self):
        """Test display_pronouns for custom pronouns."""
        person = Person.objects.create(
            full_name="Jane Doe",
            pronouns="other",
            custom_pronouns="fae/faer",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.display_pronouns, "fae/faer")

    def test_display_pronouns_property_empty(self):
        """Test display_pronouns when no pronouns set."""
        person = Person.objects.create(
            full_name="Jane Doe", created_by=self.user, updated_by=self.user
        )

        self.assertEqual(person.display_pronouns, "")

    def test_get_name_for_sorting_family_names(self):
        """Test get_name_for_sorting with family names."""
        person = Person.objects.create(
            full_name="Jane Doe",
            given_names="Jane",
            family_names="Doe",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.get_name_for_sorting(), "Doe, Jane")

    def test_get_name_for_sorting_no_family_names(self):
        """Test get_name_for_sorting without family names."""
        person = Person.objects.create(
            full_name="Jane Doe", created_by=self.user, updated_by=self.user
        )

        self.assertEqual(person.get_name_for_sorting(), "Jane Doe")

    def test_str_method(self):
        """Test the __str__ method returns display_name."""
        person = Person.objects.create(
            full_name="Jane Doe",
            preferred_name="Jane",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(str(person), "Jane")

    def test_gender_choices_validation(self):
        """Test that gender_identity accepts valid choices."""
        valid_genders = [
            "woman",
            "man",
            "non_binary",
            "genderfluid",
            "agender",
            "questioning",
            "other",
            "prefer_not_to_say",
        ]

        for gender in valid_genders:
            person = Person.objects.create(
                full_name=f"Test Person {gender}",
                gender_identity=gender,
                created_by=self.user,
                updated_by=self.user,
            )
            self.assertEqual(person.gender_identity, gender)

    def test_sex_choices_validation(self):
        """Test that biological_sex accepts valid choices."""
        valid_sexes = ["female", "male", "intersex", "unknown", "prefer_not_to_say"]

        for sex in valid_sexes:
            person = Person.objects.create(
                full_name=f"Test Person {sex}",
                biological_sex=sex,
                created_by=self.user,
                updated_by=self.user,
            )
            self.assertEqual(person.biological_sex, sex)

    def test_pronoun_choices_validation(self):
        """Test that pronouns accepts valid choices."""
        valid_pronouns = [
            "she_her",
            "he_him",
            "they_them",
            "xe_xir",
            "ze_zir",
            "other",
            "ask_me",
        ]

        for pronoun in valid_pronouns:
            person = Person.objects.create(
                full_name=f"Test Person {pronoun}",
                pronouns=pronoun,
                created_by=self.user,
                updated_by=self.user,
            )
            self.assertEqual(person.pronouns, pronoun)

    def test_save_with_user_new_record(self):
        """Test save method with user parameter for new record."""
        person = Person(full_name="Jane Doe")
        person.save(user=self.user)

        self.assertEqual(person.created_by, self.user)
        self.assertEqual(person.updated_by, self.user)

    def test_save_with_user_existing_record(self):
        """Test save method with user parameter for existing record."""
        person = Person.objects.create(
            full_name="Jane Doe", created_by=self.user, updated_by=self.user
        )

        # Create another user for update
        test_password = "testpass123"  # noqa: S105
        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password=test_password
        )

        person.full_name = "Jane Smith"
        person.save(user=other_user)

        # created_by should remain the same, updated_by should change
        self.assertEqual(person.created_by, self.user)
        self.assertEqual(person.updated_by, other_user)

    def test_db_table_name(self):
        """Test that the model uses the correct database table name."""
        self.assertEqual(Person._meta.db_table, "person")

    def test_required_fields(self):
        """Test that required fields must be provided."""
        # Test that we can't create a Person without created_by and updated_by
        with self.assertRaises(IntegrityError):
            Person.objects.create(full_name="Jane Doe")

    def test_max_length_constraints(self):
        """Test field max_length constraints."""
        # Test full_name max_length
        long_name = "a" * 201  # 201 characters, exceeds 200 limit

        person = Person(full_name=long_name, created_by=self.user, updated_by=self.user)

        with self.assertRaises(ValidationError):
            person.full_clean()

    def test_blank_fields_allowed(self):
        """Test that fields marked as blank=True can be empty."""
        person = Person.objects.create(
            full_name="Jane Doe",
            given_names="",  # blank=True
            family_names="",  # blank=True
            preferred_name="",  # blank=True
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertEqual(person.given_names, "")
        self.assertEqual(person.family_names, "")
        self.assertEqual(person.preferred_name, "")
