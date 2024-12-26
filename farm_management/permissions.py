from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .models import Farm, Cow, MilkProduction, VeterinaryRecord

def create_default_groups():
    # Farm Owner Group
    owner_group, _ = Group.objects.get_or_create(name='Farm Owner')
    
    # Farm Manager Group
    manager_group, _ = Group.objects.get_or_create(name='Farm Manager')
    
    # Farm Worker Group
    worker_group, _ = Group.objects.get_or_create(name='Farm Worker')

    # Get content types
    farm_ct = ContentType.objects.get_for_model(Farm)
    cow_ct = ContentType.objects.get_for_model(Cow)
    milk_ct = ContentType.objects.get_for_model(MilkProduction)
    vet_ct = ContentType.objects.get_for_model(VeterinaryRecord)

    # Define permissions for each group
    owner_permissions = [
        # Farm permissions
        Permission.objects.get(codename='add_farm', content_type=farm_ct),
        Permission.objects.get(codename='change_farm', content_type=farm_ct),
        Permission.objects.get(codename='delete_farm', content_type=farm_ct),
        Permission.objects.get(codename='view_farm', content_type=farm_ct),
        # Cow permissions
        Permission.objects.get(codename='add_cow', content_type=cow_ct),
        Permission.objects.get(codename='change_cow', content_type=cow_ct),
        Permission.objects.get(codename='delete_cow', content_type=cow_ct),
        Permission.objects.get(codename='view_cow', content_type=cow_ct),
        # All other model permissions...
    ]

    manager_permissions = [
        # Farm permissions (view only)
        Permission.objects.get(codename='view_farm', content_type=farm_ct),
        # Cow permissions
        Permission.objects.get(codename='add_cow', content_type=cow_ct),
        Permission.objects.get(codename='change_cow', content_type=cow_ct),
        Permission.objects.get(codename='view_cow', content_type=cow_ct),
        # Milk production permissions
        Permission.objects.get(codename='add_milkproduction', content_type=milk_ct),
        Permission.objects.get(codename='change_milkproduction', content_type=milk_ct),
        Permission.objects.get(codename='view_milkproduction', content_type=milk_ct),
        # Vet record permissions
        Permission.objects.get(codename='add_veterinaryrecord', content_type=vet_ct),
        Permission.objects.get(codename='change_veterinaryrecord', content_type=vet_ct),
        Permission.objects.get(codename='view_veterinaryrecord', content_type=vet_ct),
    ]

    worker_permissions = [
        # View-only permissions for all models
        Permission.objects.get(codename='view_cow', content_type=cow_ct),
        Permission.objects.get(codename='view_milkproduction', content_type=milk_ct),
        Permission.objects.get(codename='view_veterinaryrecord', content_type=vet_ct),
        # Add milk production records
        Permission.objects.get(codename='add_milkproduction', content_type=milk_ct),
    ]

    # Assign permissions to groups
    owner_group.permissions.set(owner_permissions)
    manager_group.permissions.set(manager_permissions)
    worker_group.permissions.set(worker_permissions)
