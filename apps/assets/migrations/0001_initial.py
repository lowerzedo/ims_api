"""Initial schema for assets domain."""
from __future__ import annotations

from decimal import Decimal
import uuid

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("clients", "0001_initial"),
        ("lookups", "0004_alter_addresstype_options_alter_businesstype_options_and_more"),
        ("policies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LossPayee",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("contact_person_name", models.CharField(blank=True, max_length=255)),
                ("telephone", models.CharField(blank=True, max_length=32)),
                ("fax", models.CharField(blank=True, max_length=32)),
                ("cell_phone", models.CharField(blank=True, max_length=32)),
                (
                    "preference",
                    models.CharField(
                        choices=[("EMAIL", "Email"), ("FAX", "Fax")],
                        default="EMAIL",
                        max_length=16,
                    ),
                ),
                ("remarks", models.TextField(blank=True)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="loss_payees",
                        to="clients.address",
                    ),
                ),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "vin",
                    models.CharField(
                        max_length=17,
                        unique=True,
                        validators=[django.core.validators.RegexValidator('^[A-HJ-NPR-Z0-9]{17}$', message='VIN must be 17 characters and exclude I, O, Q.')],
                    ),
                ),
                ("unit_number", models.CharField(blank=True, max_length=64)),
                (
                    "year",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1900),
                            django.core.validators.MaxValueValidator(2100),
                        ]
                    ),
                ),
                ("make", models.CharField(max_length=128)),
                ("model", models.CharField(max_length=128)),
                (
                    "gvw",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Gross Vehicle Weight"),
                ),
                (
                    "pd_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Physical damage value.",
                        max_digits=12,
                        null=True,
                    ),
                ),
                (
                    "deductible",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vehicles",
                        to="clients.client",
                    ),
                ),
                (
                    "loss_payee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vehicles",
                        to="assets.losspayee",
                    ),
                ),
                (
                    "vehicle_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicles",
                        to="lookups.vehicletype",
                    ),
                ),
            ],
            options={"ordering": ("unit_number", "vin")},
        ),
        migrations.CreateModel(
            name="PolicyVehicle",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                            ("unassigned", "Unassigned"),
                        ],
                        default="active",
                        max_length=16,
                    ),
                ),
                ("inception_date", models.DateField(blank=True, null=True)),
                ("termination_date", models.DateField(blank=True, null=True)),
                (
                    "garaging_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="policy_vehicle_garaging",
                        to="clients.address",
                    ),
                ),
                (
                    "policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="policy_vehicles",
                        to="policies.policy",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="policy_assignments",
                        to="assets.vehicle",
                    ),
                ),
            ],
            options={
                "ordering": ("policy", "vehicle"),
                "unique_together": {("policy", "vehicle")},
            },
        ),
    ]
