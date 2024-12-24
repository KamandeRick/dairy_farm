from django.contrib import admin
from .models import Cow, MilkProduction, VeterinaryRecord

admin.site.register(Cow)
admin.site.register(MilkProduction)
admin.site.register(VeterinaryRecord)
