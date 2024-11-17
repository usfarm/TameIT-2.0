# backend/api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Subscription, Organization, OrganizationMembership,
    Project, APIKey, Usage, AuditLog
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'company', 'is_premium', 'is_staff')
    list_filter = ('is_premium', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('SAAS Info', {'fields': ('company', 'is_premium')}),
    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan_type', 'is_active')
    search_fields = ('user__email', 'user__username')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email')

@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'joined_at')
    list_filter = ('role',)
    search_fields = ('user__email', 'organization__name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_by', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'organization__name')

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'organization', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'user__email', 'organization__name')
    readonly_fields = ('key',)

@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'resource_type', 'quantity', 'date')
    list_filter = ('resource_type', 'date')
    search_fields = ('user__email', 'organization__name')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'action', 'resource_type', 'created_at')
    list_filter = ('action', 'resource_type', 'created_at')
    search_fields = ('user__email', 'organization__name', 'resource_id')
    readonly_fields = ('created_at',)