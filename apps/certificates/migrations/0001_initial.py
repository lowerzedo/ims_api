# Generated manually for certificates app
from __future__ import annotations

import uuid

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import apps.certificates.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("clients", "0001_initial"),
        ("policies", "0002_alter_policy_account_manager_rate"),
        ("assets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CertificateHolder",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("contact_person", models.CharField(blank=True, max_length=255)),
                ("phone_number", models.CharField(blank=True, max_length=32)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="certificate_holders",
                        to="clients.address",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="MasterCertificate",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("settings", models.JSONField(blank=True, default=dict)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="master_certificates_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="master_certificates",
                        to="policies.policy",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="master_certificates_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "unique_together": {("policy", "name")},
            },
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("verification_code", models.CharField(editable=False, max_length=20, unique=True)),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        max_length=512,
                        null=True,
                        upload_to=apps.certificates.models.certificate_document_upload_to,
                    ),
                ),
                (
                    "certificate_holder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="certificates",
                        to="certificates.certificateholder",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="certificates_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "master_certificate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certificates",
                        to="certificates.mastercertificate",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="certificates_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="CertificateVehicle",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "certificate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certificate_vehicles",
                        to="certificates.certificate",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vehicle_certificates",
                        to="assets.vehicle",
                    ),
                ),
            ],
            options={
                "ordering": ("certificate", "vehicle"),
                "unique_together": {("certificate", "vehicle")},
            },
        ),
        migrations.CreateModel(
            name="CertificateDriver",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "certificate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certificate_drivers",
                        to="certificates.certificate",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="driver_certificates",
                        to="assets.driver",
                    ),
                ),
            ],
            options={
                "ordering": ("certificate", "driver"),
                "unique_together": {("certificate", "driver")},
            },
        ),
        migrations.AddField(
            model_name="certificate",
            name="drivers",
            field=models.ManyToManyField(
                blank=True,
                related_name="certificates",
                through="certificates.CertificateDriver",
                to="assets.driver",
            ),
        ),
        migrations.AddField(
            model_name="certificate",
            name="vehicles",
            field=models.ManyToManyField(
                blank=True,
                related_name="certificates",
                through="certificates.CertificateVehicle",
                to="assets.vehicle",
            ),
        ),
    ]
