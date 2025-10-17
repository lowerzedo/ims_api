"""Populate initial lookup data."""
from django.db import migrations


def seed_lookups(apps, schema_editor):
    policy_statuses = [
        {"name": "Active", "description": "Policy currently in force."},
        {"name": "Inactive", "description": "Policy no longer active."},
        {"name": "Prospect", "description": "Potential client policy."},
    ]

    simple_lists = {
        "BusinessType": ["New Business", "Renewal"],
        "InsuranceType": ["Package", "Auto Liability", "MTC"],
        "PolicyType": ["Scheduled", "Reporting", "Mileage"],
        "FinanceCompany": ["Imperial PFS", "Honor Capital"],
        "ContactType": ["Owner", "Safety", "Admin", "Dispatch"],
        "AddressType": ["Physical", "Mailing", "Garaging"],
        "VehicleType": ["Truck Tractor", "Trailer", "Box Truck"],
        "LicenseClass": ["A", "B", "C"],
        "DocumentType": ["CDL", "MVR", "PFA", "Lease Agreement"],
    }

    PolicyStatus = apps.get_model("lookups", "PolicyStatus")
    for item in policy_statuses:
        PolicyStatus.objects.update_or_create(
            name=item["name"],
            defaults={"description": item["description"], "is_active": True},
        )

    for model_name, values in simple_lists.items():
        model = apps.get_model("lookups", model_name)
        for value in values:
            model.objects.update_or_create(name=value, defaults={"is_active": True})


def unseed_lookups(apps, schema_editor):
    models = [
        "PolicyStatus",
        "BusinessType",
        "InsuranceType",
        "PolicyType",
        "FinanceCompany",
        "ContactType",
        "AddressType",
        "VehicleType",
        "LicenseClass",
        "DocumentType",
    ]
    for model_name in models:
        model = apps.get_model("lookups", model_name)
        model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("lookups", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_lookups, reverse_code=unseed_lookups),
    ]
