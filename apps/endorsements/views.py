"""API views for endorsements."""
from __future__ import annotations

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Endorsement, EndorsementChange
from .serializers import EndorsementChangeSerializer, EndorsementSerializer


class BaseSoftDeleteViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in {"true", "1", "yes"}:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])


class EndorsementViewSet(BaseSoftDeleteViewSet):
    serializer_class = EndorsementSerializer
    queryset = Endorsement.objects.select_related(
        "policy",
        "policy__client",
        "created_by",
        "updated_by",
    ).prefetch_related("changes")
    filterset_fields = {
        "policy": ["exact"],
        "status": ["exact"],
        "current_stage": ["exact"],
    }
    search_fields = ("name", "policy__policy_number", "policy__client__company_name")
    ordering_fields = ("created_at", "updated_at", "effective_date")
    ordering = ("-created_at",)

    def perform_create(self, serializer: EndorsementSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer: EndorsementSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(updated_by=user)

    @action(detail=True, methods=["post"], url_path="start")
    def start(self, request, *args, **kwargs):
        endorsement = self.get_object()
        if endorsement.status not in {Endorsement.Status.DRAFT, Endorsement.Status.IN_PROGRESS}:
            raise serializers.ValidationError("Only draft endorsements can be started.")
        endorsement.status = Endorsement.Status.IN_PROGRESS
        stage = request.data.get("stage")
        if stage:
            if stage not in dict(Endorsement.Stage.choices):
                raise serializers.ValidationError("Invalid stage supplied.")
            endorsement.current_stage = stage
        endorsement.updated_by = request.user
        endorsement.save(update_fields=["status", "current_stage", "updated_by", "updated_at"])
        return Response(self.get_serializer(endorsement).data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, *args, **kwargs):
        endorsement = self.get_object()
        if endorsement.status == Endorsement.Status.COMPLETED:
            raise serializers.ValidationError("Endorsement already completed.")
        endorsement.mark_completed(user=request.user)
        return Response(self.get_serializer(endorsement).data)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, *args, **kwargs):
        endorsement = self.get_object()
        if endorsement.status == Endorsement.Status.CANCELLED:
            raise serializers.ValidationError("Endorsement already cancelled.")
        reason = request.data.get("reason")
        endorsement.mark_cancelled(user=request.user, reason=reason)
        return Response(self.get_serializer(endorsement).data)

    @action(detail=True, methods=["post"], url_path="advance")
    def advance(self, request, *args, **kwargs):
        endorsement = self.get_object()
        stage = request.data.get("stage")
        if stage not in dict(Endorsement.Stage.choices):
            raise serializers.ValidationError("Invalid stage supplied.")
        endorsement.current_stage = stage
        endorsement.status = Endorsement.Status.IN_PROGRESS
        endorsement.updated_by = request.user
        endorsement.save(update_fields=["current_stage", "status", "updated_by", "updated_at"])
        return Response(self.get_serializer(endorsement).data)


class EndorsementChangeViewSet(BaseSoftDeleteViewSet):
    serializer_class = EndorsementChangeSerializer
    queryset = EndorsementChange.objects.select_related(
        "endorsement",
        "endorsement__policy",
        "created_by",
    )
    filterset_fields = {
        "endorsement": ["exact"],
        "change_type": ["exact"],
        "stage": ["exact"],
    }
    ordering_fields = ("created_at", "updated_at")
    ordering = ("created_at",)

    def perform_create(self, serializer: EndorsementChangeSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user)

    def perform_update(self, serializer: EndorsementChangeSerializer) -> None:
        serializer.save()
