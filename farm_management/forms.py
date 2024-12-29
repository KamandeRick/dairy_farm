from django import forms
from .models import Cow, MilkProduction, VeterinaryRecord

class CowForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = ['tag_number', 'name', 'breed', 'date_of_birth', 'status', 'weight', 'current_lactation']

class MilkProductionForm(forms.ModelForm):
    class Meta:
        model = MilkProduction
        fields = ['cow', 'date', 'morning_amount', 'evening_amount', 'fat_content', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['morning_amount'].required = False
        self.fields['evening_amount'].required = False
        self.fields['fat_content'].required = False
        self.fields['notes'].required = False


class VeterinaryRecordForm(forms.ModelForm):
    class Meta:
        model = VeterinaryRecord
        fields = ['cow', 'date', 'record_type', 'diagnosis', 'treatment', 'medicine_given', 'dosage', 'cost', 'next_visit_date', 'veterinarian', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'next_visit_date': forms.DateInput(attrs={'type': 'date'})
        }
