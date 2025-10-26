"""Utilities for generating certificate documents."""
from __future__ import annotations

from typing import Iterable

from django.utils import timezone

from apps.certificates.models import Certificate


def _escape_pdf_text(content: str) -> str:
    return content.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_pdf(lines: list[str]) -> bytes:
    objects: list[bytes] = []

    # Catalog
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    # Pages
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")

    # Content stream will be object 4
    # Page references content stream object 4 and Helvetica font (object 5)
    page_dict = (
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
    )
    objects.append(page_dict)

    line_height = 16
    y_position = 760
    content_segments = []
    for raw_line in lines:
        safe_line = _escape_pdf_text(raw_line)
        segment = f"BT /F1 12 Tf 50 {y_position} Td ({safe_line}) Tj ET"
        content_segments.append(segment)
        y_position -= line_height

    content_stream = "\n".join(content_segments).encode("latin-1")
    stream_obj = (
        f"<< /Length {len(content_stream)} >>\nstream\n".encode("latin-1")
        + content_stream
        + b"\nendstream"
    )
    objects.append(stream_obj)

    # Font definition
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("latin-1"))
        pdf.extend(obj if isinstance(obj, (bytes, bytearray)) else obj.encode("latin-1"))
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    total_objects = len(objects) + 1
    pdf.extend(f"xref\n0 {total_objects}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {total_objects} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF"
        ).encode("latin-1")
    )

    return bytes(pdf)


def render_certificate_pdf(certificate: Certificate, *, vehicles: Iterable, drivers: Iterable) -> bytes:
    """Render a lightweight PDF summary for a certificate."""

    policy = certificate.master_certificate.policy
    holder = certificate.certificate_holder
    issued_at = timezone.localtime(certificate.created_at)

    lines = [
        "Insurance Management System",
        "Certificate of Insurance",
        "",
        f"Certificate #: {certificate.verification_code}",
        f"Issued: {issued_at.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"Policy: {policy.policy_number}",
        f"Client: {policy.client.company_name}",
        "",
        "Certificate Holder:",
        f"  {holder.name}",
    ]

    if holder.contact_person:
        lines.append(f"  Contact: {holder.contact_person}")
    if holder.email:
        lines.append(f"  Email: {holder.email}")
    if holder.phone_number:
        lines.append(f"  Phone: {holder.phone_number}")

    address = holder.address
    lines.append(
        f"  Address: {address.street_address}, {address.city}, {address.state} {address.zip_code}"
    )

    lines.append("")
    lines.append("Vehicles")
    vehicle_list = list(vehicles)
    if vehicle_list:
        for vehicle in vehicle_list:
            pd_value = (
                f" (PD ${vehicle.pd_amount:,.2f})" if getattr(vehicle, "pd_amount", None) else ""
            )
            lines.append(
                f"  {vehicle.unit_number or vehicle.vin} - {vehicle.year} {vehicle.make} {vehicle.model}{pd_value}"
            )
    else:
        lines.append("  None selected")

    lines.append("")
    lines.append("Drivers")
    driver_list = list(drivers)
    if driver_list:
        for driver in driver_list:
            lines.append(f"  {driver.first_name} {driver.last_name} - License {driver.license_state} {driver.license_number}")
    else:
        lines.append("  None selected")

    lines.append("")
    lines.append("Verification")
    lines.append(
        "  Present this certificate along with the verification code for authenticity checks."
    )

    return _build_pdf(lines)
