from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Farm

class FarmUserMixin(UserPassesTestMixin):
    """Ensure user has access to this farm"""
    def test_func(self):
<<<<<<< HEAD
        # Get farm from user's ownership or related farm
        user_farms = Farm.objects.filter(owner=self.request.user)
        if user_farms.exists():
            return True
        # Check if user is manager or worker
        return self.request.user.groups.filter(name__in=['Farm Manager', 'Farm Worker']).exists()
=======
        farm_id = self.kwargs.get('farm_id') or self.request.GET.get('farm_id')
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            return self.request.user == farm.owner or \
                   self.request.user.groups.filter(name__in=['Farm Manager', 'Farm Worker']).exists()
        return False
>>>>>>> 8d55bc62081881fbf1501bb381c39602f20b88f8

class FarmManagerMixin(UserPassesTestMixin):
    """Ensure user is farm owner or manager"""
    def test_func(self):
<<<<<<< HEAD
        # Get farm from user's ownership
        user_farms = Farm.objects.filter(owner=self.request.user)
        if user_farms.exists():
            return True
        # Check if user is manager
        return self.request.user.groups.filter(name='Farm Manager').exists()
=======
        farm_id = self.kwargs.get('farm_id') or self.request.GET.get('farm_id')
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            return self.request.user == farm.owner or \
                   self.request.user.groups.filter(name='Farm Manager').exists()
        return False
>>>>>>> 8d55bc62081881fbf1501bb381c39602f20b88f8

class FarmOwnerMixin(UserPassesTestMixin):
    """Ensure user is farm owner"""
    def test_func(self):
<<<<<<< HEAD
        # Get farm from user's ownership
        return Farm.objects.filter(owner=self.request.user).exists()
=======
        farm_id = self.kwargs.get('farm_id') or self.request.GET.get('farm_id')
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            return self.request.user == farm.owner
        return False
>>>>>>> 8d55bc62081881fbf1501bb381c39602f20b88f8
