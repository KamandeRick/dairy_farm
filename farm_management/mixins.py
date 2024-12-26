from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Farm

class FarmUserMixin(UserPassesTestMixin):
    """Ensure user has access to this farm"""
    def test_func(self):
        # Get farm from user's ownership or related farm
        user_farms = Farm.objects.filter(owner=self.request.user)
        if user_farms.exists():
            return True
        # Check if user is manager or worker
        return self.request.user.groups.filter(name__in=['Farm Manager', 'Farm Worker']).exists()

class FarmManagerMixin(UserPassesTestMixin):
    """Ensure user is farm owner or manager"""
    def test_func(self):
        # Get farm from user's ownership
        user_farms = Farm.objects.filter(owner=self.request.user)
        if user_farms.exists():
            return True
        # Check if user is manager
        return self.request.user.groups.filter(name='Farm Manager').exists()

class FarmOwnerMixin(UserPassesTestMixin):
    """Ensure user is farm owner"""
    def test_func(self):
        # Get farm from user's ownership
        return Farm.objects.filter(owner=self.request.user).exists()
