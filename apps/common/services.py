"""Services for creating activity logs."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from django.utils import timezone

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.assets.models import Driver, Vehicle
    from apps.clients.models import Client
    from apps.endorsements.models import Endorsement
    from apps.policies.models import Policy

from .models import ActivityLog


def log_activity(
    action_type: str,
    transaction_name: str,
    *,
    description: str = "",
    notes: str = "",
    client: "Client | None" = None,
    policy: "Policy | None" = None,
    endorsement: "Endorsement | None" = None,
    vehicle: "Vehicle | None" = None,
    driver: "Driver | None" = None,
    performed_by: "User | None" = None,
    metadata: dict | None = None,
    timestamp: datetime | None = None,
) -> ActivityLog:
    """
    Create an activity log entry.

    Example usage:
        log_activity(
            ActivityLog.ActionType.VEHICLE_ASSIGNED,
            f"Vehicle {vehicle.vin} assigned",
            description=f"Truck VIN {vehicle.vin} was assigned to policy {policy.carrier_product.insurance_company_name}, "
                        f"Policy Number {policy.policy_number} on {timezone.now().strftime('%m/%d/%Y %I:%M:%S %p')} "
                        f"by {user.full_name}",
            client=policy.client,
            policy=policy,
            vehicle=vehicle,
            performed_by=user,
        )
    """
    return ActivityLog.objects.create(
        action_type=action_type,
        transaction_name=transaction_name,
        description=description,
        notes=notes,
        client=client,
        policy=policy,
        endorsement=endorsement,
        vehicle=vehicle,
        driver=driver,
        performed_by=performed_by,
        metadata=metadata or {},
        timestamp=timestamp or timezone.now(),
    )


def format_log_description(
    action: str,
    *,
    vehicle: "Vehicle | None" = None,
    driver: "Driver | None" = None,
    policy: "Policy | None" = None,
    user: "User | None" = None,
    timestamp: datetime | None = None,
) -> str:
    """
    Generate auto-formatted log trail description.

    Example output:
    "Truck VIN 4V4NC912GLR321551 was assigned to policy Trinity / Lloyd's,
     Policy Number 238394-001APD-93755 on 09/24/2025 09:37:46 AM by Amir Mambetaliev"
    """
    ts = timestamp or timezone.now()
    time_str = ts.strftime("%m/%d/%Y %I:%M:%S %p")
    user_name = user.full_name if user else "System"

    parts = []

    if vehicle:
        parts.append(f"Truck VIN {vehicle.vin}")

    if driver:
        parts.append(f"Driver {driver.first_name} {driver.last_name}")

    parts.append(f"was {action}")

    if policy:
        carrier = policy.carrier_product.insurance_company_name if policy.carrier_product else "Unknown Carrier"
        parts.append(f"to policy {carrier}, Policy Number {policy.policy_number}")

    parts.append(f"on {time_str} by {user_name}")

    return " ".join(parts)


# Convenience functions for common actions


def log_client_created(client: "Client", user: "User | None" = None) -> ActivityLog:
    """Log client creation."""
    return log_activity(
        ActivityLog.ActionType.CLIENT_CREATED,
        f"Client Created: {client.company_name}",
        description=f"Client {client.company_name} was created on "
        f"{timezone.now().strftime('%m/%d/%Y %I:%M:%S %p')} by {user.full_name if user else 'System'}",
        client=client,
        performed_by=user,
    )


def log_policy_created(policy: "Policy", user: "User | None" = None) -> ActivityLog:
    """Log policy creation."""
    carrier = policy.carrier_product.insurance_company_name if policy.carrier_product else "Unknown"
    return log_activity(
        ActivityLog.ActionType.POLICY_CREATED,
        f"Policy Created: {policy.policy_number}",
        description=f"Policy {policy.policy_number} ({carrier}) was created on "
        f"{timezone.now().strftime('%m/%d/%Y %I:%M:%S %p')} by {user.full_name if user else 'System'}",
        client=policy.client,
        policy=policy,
        performed_by=user,
    )


def log_vehicle_assigned(
    vehicle: "Vehicle", policy: "Policy", user: "User | None" = None
) -> ActivityLog:
    """Log vehicle assignment to policy."""
    carrier = policy.carrier_product.insurance_company_name if policy.carrier_product else "Unknown"
    return log_activity(
        ActivityLog.ActionType.VEHICLE_ASSIGNED,
        f"Vehicle Assigned: {vehicle.vin}",
        description=format_log_description(
            "assigned", vehicle=vehicle, policy=policy, user=user
        ),
        client=policy.client,
        policy=policy,
        vehicle=vehicle,
        performed_by=user,
    )


def log_driver_assigned(
    driver: "Driver", policy: "Policy", user: "User | None" = None
) -> ActivityLog:
    """Log driver assignment to policy."""
    return log_activity(
        ActivityLog.ActionType.DRIVER_ASSIGNED,
        f"Driver Assigned: {driver.first_name} {driver.last_name}",
        description=format_log_description(
            "assigned", driver=driver, policy=policy, user=user
        ),
        client=policy.client,
        policy=policy,
        driver=driver,
        performed_by=user,
    )


def log_endorsement_created(
    endorsement: "Endorsement", user: "User | None" = None
) -> ActivityLog:
    """Log endorsement creation."""
    policy = endorsement.policy
    return log_activity(
        ActivityLog.ActionType.ENDORSEMENT_CREATED,
        endorsement.name,
        description=f"Endorsement '{endorsement.name}' was created for policy {policy.policy_number} on "
        f"{timezone.now().strftime('%m/%d/%Y %I:%M:%S %p')} by {user.full_name if user else 'System'}",
        client=policy.client,
        policy=policy,
        endorsement=endorsement,
        performed_by=user,
    )


def log_endorsement_completed(
    endorsement: "Endorsement", user: "User | None" = None
) -> ActivityLog:
    """Log endorsement completion."""
    policy = endorsement.policy
    return log_activity(
        ActivityLog.ActionType.ENDORSEMENT_COMPLETED,
        f"Endorsement Completed: {endorsement.name}",
        description=f"Endorsement '{endorsement.name}' was completed on "
        f"{timezone.now().strftime('%m/%d/%Y %I:%M:%S %p')} by {user.full_name if user else 'System'}",
        client=policy.client,
        policy=policy,
        endorsement=endorsement,
        performed_by=user,
    )


def log_endorsement_cancelled(
    endorsement: "Endorsement", user: "User | None" = None, reason: str = ""
) -> ActivityLog:
    """Log endorsement cancellation."""
    policy = endorsement.policy
    return log_activity(
        ActivityLog.ActionType.ENDORSEMENT_CANCELLED,
        f"Endorsement Cancelled: {endorsement.name}",
        description=f"Endorsement '{endorsement.name}' was cancelled on "
        f"{timezone.now().strftime('%m/%d/%Y %I:%M:%S %p')} by {user.full_name if user else 'System'}",
        notes=reason,
        client=policy.client,
        policy=policy,
        endorsement=endorsement,
        performed_by=user,
    )

