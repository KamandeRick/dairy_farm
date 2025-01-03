from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Farm(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        permissions = [
            ("manage_farm", "Can manage farm settings"),
            ("manage_workers", "Can manage farm workers"),
            ("view_reports", "Can view farm reports"),
        ]

    def __str__(self):
        return self.name

class Cow(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DRY', 'Dry'),
        ('SOLD', 'Sold'),
        ('DECEASED', 'Deceased')
    ]
    
    BREED_CHOICES = [
        ('FRIESIAN', 'Friesian'),
        ('AYRSHIRE', 'Ayrshire'),
        ('JERSEY', 'Jersey'),
        ('GUERNSEY', 'Guernsey')
    ]


    # Add farm relationship
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='cows',  null=True, blank=True)

    # Basic Information
    tag_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True)
    breed = models.CharField(max_length=20, choices=BREED_CHOICES)
    date_of_birth = models.DateField()
    date_acquired = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Additional Details
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    current_lactation = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tag_number} - {self.name}"

    class Meta:
        ordering = ['tag_number']
        unique_together = ['farm', 'tag_number']

class MilkProduction(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milk_records')
    date = models.DateField(default=timezone.now)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Morning Production
    morning_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Evening Production
    evening_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Quality Metrics
    fat_content = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    
    notes = models.TextField(blank=True)

    @property
    def total_production(self):
        return self.morning_amount + self.evening_amount

    def __str__(self):
        return f"{self.cow.tag_number} - {self.date}"

    class Meta:
        ordering = ['-date']
        unique_together = ['cow', 'date']

class VeterinaryRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('CHECKUP', 'Regular Checkup'),
        ('TREATMENT', 'Treatment'),
        ('VACCINATION', 'Vaccination'),
        ('DEWORMING', 'Deworming'),
        ('INJURY', 'Injury'),
        ('OTHER', 'Other')
    ]

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='vet_records')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    medicine_given = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    next_visit_date = models.DateField(null=True, blank=True)
    
    veterinarian = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cow.tag_number} - {self.record_type} - {self.date}"

    class Meta:
        ordering = ['-date']
