# backend/api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Extended user model for SAAS platform"""
    company = models.CharField(max_length=100, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subscription(models.Model):
    """Subscription model for managing user plans"""
    PLAN_TYPES = [
        ('FREE', 'Free'),
        ('BASIC', 'Basic'),
        ('PRO', 'Professional'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='FREE')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan_type}"

class Organization(models.Model):
    """Organization model for team/company management"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_organizations')
    members = models.ManyToManyField(User, through='OrganizationMembership')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class OrganizationMembership(models.Model):
    """Through model for Organization-User relationship"""
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MEMBER', 'Member'),
        ('VIEWER', 'Viewer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'organization')

class Project(models.Model):
    """Project model for organizing work within organizations"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class APIKey(models.Model):
    """API key management for users/organizations"""
    key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"

class Usage(models.Model):
    """Track API/resource usage for billing purposes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    resource_type = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'organization', 'resource_type', 'date')

class AuditLog(models.Model):
    """Audit logging for important actions"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=50)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)