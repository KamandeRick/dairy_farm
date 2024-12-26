from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Farm

class FarmUserMixin(UserPassesTestMixin):
    """Ensure user has access to this farm"""
    def test_func(self):
        farm_id = self.kwargs.get('farm_id') or self.request.GET.get('farm_id')
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            return self.request.user == farm.owner or \
                   self.request.user.groups.filter(name__in=['Farm Manager', 'Farm Worker']).exists()
        return False

class FarmManagerMixin(UserPassesTestMixin):
    """Ensure user is farm owner or manager"""
    def test_func(self):
        farm_id = self.kwargs.get('farm_id') or self.request.GET.get('farm_id')
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            return self.request.user == farm.owner or \
                   self.request.user.groups.filter(name='Farm Manager').exists()
        return False

class FarmOwnerMixin(UserPassesTestMixin):
    """Ensure user is farm owner"""
    def test_func(self):
        farm_id = self.kwargs.get('farm_id') or self.request.GET.get('farm_id')
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            return self.request.user == farm.owner
        return False
