from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Farm, Cow, MilkProduction, VeterinaryRecord
from .forms import CowForm, MilkProductionForm, VeterinaryRecordForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a farm for the new user
            Farm.objects.create(
                name=f"{user.username}'s Farm",
                owner=user
            )
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get or create the user's farm
    farm, created = Farm.objects.get_or_create(
        owner=request.user,
        defaults={'name': f"{request.user.username}'s Farm"}
    )
    
    total_cows = Cow.objects.filter(farm=farm).count()
    active_cows = Cow.objects.filter(farm=farm, status='ACTIVE').count()
    latest_milk_records = MilkProduction.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')[:5]
    recent_vet_records = VeterinaryRecord.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')[:5]
    
    context = {
        'farm': farm,
        'total_cows': total_cows,
        'active_cows': active_cows,
        'latest_milk_records': latest_milk_records,
        'recent_vet_records': recent_vet_records,
    }
    return render(request, 'farm_management/dashboard.html', context)

@login_required
def cow_list(request):
    farm = request.user.farm_set.first()
    cows = Cow.objects.filter(farm=farm)
    return render(request, 'farm_management/cow_list.html', {'cows': cows})

@login_required
def cow_detail(request, tag_number):
    farm = request.user.farm_set.first()
    cow = get_object_or_404(Cow, farm=farm, tag_number=tag_number)
    milk_records = cow.milk_records.order_by('-date')[:10]
    vet_records = cow.vet_records.order_by('-date')[:10]
    
    context = {
        'cow': cow,
        'milk_records': milk_records,
        'vet_records': vet_records,
    }
    return render(request, 'farm_management/cow_detail.html', context)

@login_required
def milk_production_list(request):
    farm = request.user.farm_set.first()
    records = MilkProduction.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')
    return render(request, 'farm_management/milk_production_list.html', {'records': records})

@login_required
def vet_record_list(request):
    farm = request.user.farm_set.first()
    records = VeterinaryRecord.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')
    return render(request, 'farm_management/vet_record_list.html', {'records': records})

@login_required
def add_cow(request):
    farm = request.user.farm_set.first()
    if request.method == 'POST':
        form = CowForm(request.POST)
        if form.is_valid():
            cow = form.save(commit=False)
            cow.farm = farm
            cow.save()
            return redirect('farm_management:cow_list')
    else:
        form = CowForm()
    return render(request, 'farm_management/cow_form.html', {'form': form})

@login_required
def add_milk_record(request):
    farm = request.user.farm_set.first()
    if request.method == 'POST':
        form = MilkProductionForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.recorded_by = request.user
            # Verify the cow belongs to the user's farm
            if record.cow.farm != farm:
                messages.error(request, "Invalid cow selection.")
                return render(request, 'farm_management/milk_production_form.html', {'form': form})
            record.save()
            return redirect('farm_management:milk_production_list')
    else:
        form = MilkProductionForm()
        # Filter cow choices to only show farm's cows
        form.fields['cow'].queryset = Cow.objects.filter(farm=farm)
    return render(request, 'farm_management/milk_production_form.html', {'form': form})

@login_required
def add_vet_record(request):
    farm = request.user.farm_set.first()
    if request.method == 'POST':
        form = VeterinaryRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.recorded_by = request.user
            # Verify the cow belongs to the user's farm
            if record.cow.farm != farm:
                messages.error(request, "Invalid cow selection.")
                return render(request, 'farm_management/vet_record_form.html', {'form': form})
            record.save()
            return redirect('farm_management:vet_record_list')
    else:
        form = VeterinaryRecordForm()
        # Filter cow choices to only show farm's cows
        form.fields['cow'].queryset = Cow.objects.filter(farm=farm)
    return render(request, 'farm_management/vet_record_form.html', {'form': form})
