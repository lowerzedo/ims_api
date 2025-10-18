"""Admin registration for endorsements."""
from __future__ import annotations

from django.contrib import admin

from .models import Endorsement, EndorsementChange, EndorsementDocument


@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "policy",
        "status",
        "current_stage",
        "effective_date",
        "premium_change",
        "created_by",
        "updated_at",
    )
    list_filter = ("status", "current_stage", "created_at")
    search_fields = ("name", "policy__policy_number", "policy__client__company_name")
    autocomplete_fields = ("policy", "created_by", "updated_by")


@admin.register(EndorsementChange)
class EndorsementChangeAdmin(admin.ModelAdmin):
    list_display = (
        "endorsement",
        "change_type",
        "stage",
        "summary",
        "created_by",
        "created_at",
    )
    list_filter = ("change_type", "stage")
    search_fields = ("summary", "endorsement__name", "endorsement__policy__policy_number")
    autocomplete_fields = ("endorsement", "created_by")


@admin.register(EndorsementDocument)
class EndorsementDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "endorsement",
        "stage",
        "document_type",
        "file",
        "uploaded_by",
        "created_at",
    )
    list_filter = ("stage", "document_type")
    search_fields = (
        "endorsement__name",
        "endorsement__policy__policy_number",
        "description",
    )
    autocomplete_fields = ("endorsement", "document_type", "uploaded_by")
