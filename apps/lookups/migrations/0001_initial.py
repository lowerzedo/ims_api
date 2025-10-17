"""Initial lookup tables."""
from django.db import migrations, models
import uuid
from django.utils import timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PolicyStatus",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
                ("description", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "db_table": "lookup_policy_statuses",
                "ordering": ("name",),
                "verbose_name": "Policy Status",
                "verbose_name_plural": "Policy Statuses",
            },
        ),
        migrations.CreateModel(
            name="BusinessType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_business_types",
                "ordering": ("name",),
                "verbose_name": "Business Type",
                "verbose_name_plural": "Business Types",
            },
        ),
        migrations.CreateModel(
            name="InsuranceType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_insurance_types",
                "ordering": ("name",),
                "verbose_name": "Insurance Type",
                "verbose_name_plural": "Insurance Types",
            },
        ),
        migrations.CreateModel(
            name="PolicyType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_policy_types",
                "ordering": ("name",),
                "verbose_name": "Policy Type",
                "verbose_name_plural": "Policy Types",
            },
        ),
        migrations.CreateModel(
            name="FinanceCompany",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_finance_companies",
                "ordering": ("name",),
                "verbose_name": "Finance Company",
                "verbose_name_plural": "Finance Companies",
            },
        ),
        migrations.CreateModel(
            name="ContactType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_contact_types",
                "ordering": ("name",),
                "verbose_name": "Contact Type",
                "verbose_name_plural": "Contact Types",
            },
        ),
        migrations.CreateModel(
            name="AddressType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_address_types",
                "ordering": ("name",),
                "verbose_name": "Address Type",
                "verbose_name_plural": "Address Types",
            },
        ),
        migrations.CreateModel(
            name="VehicleType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_vehicle_types",
                "ordering": ("name",),
                "verbose_name": "Vehicle Type",
                "verbose_name_plural": "Vehicle Types",
            },
        ),
        migrations.CreateModel(
            name="LicenseClass",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_license_classes",
                "ordering": ("name",),
                "verbose_name": "License Class",
                "verbose_name_plural": "License Classes",
            },
        ),
        migrations.CreateModel(
            name="DocumentType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "db_table": "lookup_document_types",
                "ordering": ("name",),
                "verbose_name": "Document Type",
                "verbose_name_plural": "Document Types",
            },
        ),
    ]
