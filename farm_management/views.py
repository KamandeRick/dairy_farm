from django.shortcuts import render, get_object_or_404, redirect
from .models import Cow, MilkProduction, VeterinaryRecord
from django.contrib.auth.decorators import login_required
from .forms import CowForm, MilkProductionForm, VeterinaryRecordForm

#def index(request):
    #"""The home page for Farm Management"""
    #return render(request, 'farm_management/index.html')

# Dashboard
@login_required
def dashboard(request):
    total_cows = Cow.objects.count()
    active_cows = Cow.objects.filter(status='ACTIVE').count()
    latest_milk_records = MilkProduction.objects.select_related('cow').order_by('-date')[:5]
    recent_vet_records = VeterinaryRecord.objects.select_related('cow').order_by('-date')[:5]

    context = {
        'total_cows': total_cows,
        'active_cows': active_cows,
        'latest_milk_records': latest_milk_records,
        'recent_vet_records': recent_vet_records,
    }
    return render(request, 'farm_management/dashboard.html', context)

# Cow Views
@login_required
def cow_list(request):
    cows = Cow.objects.all()
    return render(request, 'farm_management/cow_list.html', {'cows': cows})

@login_required
def cow_detail(request, tag_number):
    cow = get_object_or_404(Cow, tag_number=tag_number)
    milk_records = cow.milk_records.order_by('-date')[:10]
    vet_records = cow.vet_records.order_by('-date')[:10]
    
    context = {
        'cow': cow,
        'milk_records': milk_records,
        'vet_records': vet_records,
    }
    return render(request, 'farm_management/cow_detail.html', context)

# Milk Production Views
@login_required
def milk_production_list(request):
    records = MilkProduction.objects.select_related('cow').order_by('-date')
    return render(request, 'farm_management/milk_production_list.html', {'records': records})

# Veterinary Record Views
@login_required
def vet_record_list(request):
    records = VeterinaryRecord.objects.select_related('cow').order_by('-date')
    return render(request, 'farm_management/vet_record_list.html', {'records': records})

# Create Views
@login_required
def add_cow(request):
    if request.method == 'POST':
        form = CowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farm_management:cow_list')
    else:
        form = CowForm()
    return render(request, 'farm_management/cow_form.html', {'form': form})

@login_required
def add_milk_record(request):
    if request.method == 'POST':
        form = MilkProductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farm_management:milk_production_list')
    else:
        form = MilkProductionForm()
    return render(request, 'farm_management/milk_production_form.html', {'form': form})

@login_required
def add_vet_record(request):
    if request.method == 'POST':
        form = VeterinaryRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farm_management:vet_record_list')
    else:
        form = VeterinaryRecordForm()
    return render(request, 'farm_management/vet_record_form.html', {'form': form})
