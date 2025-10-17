"""Admin configuration for client domain."""
from __future__ import annotations

from django.contrib import admin

from .models import Address, Client, ClientAddress, ClientDBA, Contact


class ClientDBAInline(admin.TabularInline):
    model = ClientDBA
    extra = 0


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class ClientAddressInline(admin.TabularInline):
    model = ClientAddress
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("company_name", "dot_number", "fein", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("company_name", "dot_number", "fein")
    inlines = [ClientDBAInline, ContactInline, ClientAddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_address", "city", "state", "zip_code")
    search_fields = ("street_address", "city", "state", "zip_code")


@admin.register(ClientDBA)
class ClientDBAAdmin(admin.ModelAdmin):
    list_display = ("client", "dba_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("dba_name", "client__company_name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("client", "first_name", "last_name", "contact_type", "is_active")
    list_filter = ("contact_type", "is_active")
    search_fields = ("first_name", "last_name", "client__company_name")


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ("client", "address", "address_type", "rating", "is_active")
    list_filter = ("address_type", "is_active")
    search_fields = ("client__company_name", "address__street_address")
