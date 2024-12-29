from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Max
from django.utils import timezone
from django import forms
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Farm, Cow, MilkProduction, VeterinaryRecord
from .forms import CowForm, MilkProductionForm, VeterinaryRecordForm
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a farm for the new user
            farm = Farm.objects.create(
                name=f"{user.username}'s Farm",
                owner=user
            )
            # Add user to Farm Owner group
            owner_group = Group.objects.get(name='Farm Owner')
            user.groups.add(owner_group)


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
    

    #basic statistics
    total_cows = Cow.objects.filter(farm=farm).count()
    active_cows = Cow.objects.filter(farm=farm, status='ACTIVE').count()

    #recent milk production
    latest_milk_records = MilkProduction.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')[:5]

    #Total milk production
    # Calculate total milk production
    today = timezone.now().date()
    total_milk = MilkProduction.objects.filter(
        cow__farm=farm
    ).aggregate(
        total=Sum('morning_amount') + Sum('evening_amount')
    )['total'] or 0

    #Recent vet records
    recent_vet_records = VeterinaryRecord.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')[:5]

    # Get upcoming vet visits
    upcoming_visits = VeterinaryRecord.objects.select_related('cow').filter(
        cow__farm=farm,
        next_visit_date__gte=today
    ).order_by('next_visit_date')[:5]
    
    # Get today's best producer
    today_best = MilkProduction.objects.filter(
        cow__farm=farm,
        date=today
    ).annotate(
        daily_total=Sum('morning_amount') + Sum('evening_amount')
    ).order_by('-daily_total').first()

    # Get last 7 days production data for the graph
    #last_7_days = []
    #for i in range(7):
        #date = today - timedelta(days=i)
        #daily_total = MilkProduction.objects.filter(
            #cow__farm=farm,
            #date=date
        #).aggregate(
            #total=Sum('morning_amount') + Sum('evening_amount')
        #)['total'] or 0
        #last_7_days.append({
            #'date': date.strftime('%Y-%m-%d'),
            #'total': float(daily_total)
        #})

    # Get last 7 days production data for the graph
    dates = []
    production_values = []
    
    for i in range(6, -1, -1):  # Last 7 days
        date = today - timedelta(days=i)
        daily_total = MilkProduction.objects.filter(
            cow__farm=farm,
            date=date
        ).aggregate(
            total=Sum('morning_amount') + Sum('evening_amount')
        )['total'] or 0
        
        dates.append(date.strftime('%Y-%m-%d'))
        production_values.append(float(daily_total))
    
    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=production_values,
        mode='lines+markers',
        name='Daily Production',
        line=dict(color='#2563eb', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Milk Production Over Last 7 Days',
        xaxis_title='Date',
        yaxis_title='Total Production (L)',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='x unified'
    )
    
    # Convert the figure to JSON for the template
    plot_div = fig.to_json()


    context = {
        'farm': farm,
        'total_cows': total_cows,
        'active_cows': active_cows,
        'total_milk': total_milk,
        'upcoming_visits': upcoming_visits,
        'today_best': today_best,
        #'production_data': json.dumps(list(reversed(last_7_days))),
        'latest_milk_records': latest_milk_records,
        'recent_vet_records': recent_vet_records,
        'plot_div': plot_div,
    }
    return render(request, 'farm_management/dashboard.html', context)

@login_required
def cow_list(request):
    farm = request.user.farm_set.first()
    cows = Cow.objects.filter(farm=farm).order_by('tag_number')
    
    # Pagination
    paginator = Paginator(cows, 10)  # Show 10 records per page
    page_number = request.GET.get('page', 1)
    
    try:
        cows = paginator.page(page_number)
    except:
        cows = paginator.page(1)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'farm_management/includes/cow_table_rows.html',
            {'cows': cows}
        )
        return JsonResponse({
            'html': html,
            'has_next': cows.has_next(),
            'has_previous': cows.has_previous(),
            'current_page': cows.number,
            'total_pages': paginator.num_pages,
        })
    
    context = {
        'cows': cows,
        'total_pages': paginator.num_pages,
        'current_page': cows.number,
        'has_previous': cows.has_previous(),
        'has_next': cows.has_next(),
        'previous_page_number': cows.previous_page_number if cows.has_previous() else 1,
        'next_page_number': cows.next_page_number if cows.has_next() else paginator.num_pages,
    }
    return render(request, 'farm_management/cow_list.html', context)

@login_required
def cow_detail(request, tag_number):
    farm = request.user.farm_set.first()
    cow = get_object_or_404(Cow, farm=farm, tag_number=tag_number)
    milk_records = cow.milk_records.order_by('-date')[:3]
    vet_records = cow.vet_records.order_by('-date')[:3]
    
    context = {
        'cow': cow,
        'milk_records': milk_records,
        'vet_records': vet_records,
    }
    return render(request, 'farm_management/cow_detail.html', context)

@login_required
def update_cow(request, tag_number):
    farm = request.user.farm_set.first()
    cow = get_object_or_404(Cow, farm=farm, tag_number=tag_number)
    
    if request.method == 'POST':
        form = CowForm(request.POST, instance=cow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cow details updated successfully.')
            return redirect('farm_management:cow_detail', tag_number=cow.tag_number)
    else:
        form = CowForm(instance=cow)
    
    return render(request, 'farm_management/cow_form.html', {
        'form': form,
        'cow': cow,
        'is_update': True
    })

@login_required
def cow_milk_history(request, tag_number):
    farm = request.user.farm_set.first()
    cow = get_object_or_404(Cow, farm=farm, tag_number=tag_number)
    milk_records = cow.milk_records.all().order_by('-date')
    
    # Calculate production statistics
    total_production = sum(record.total_production for record in milk_records)
    avg_production = total_production / milk_records.count() if milk_records.count() > 0 else 0

    # Pagination
    paginator = Paginator(milk_records, 10)  # 10 records per page
    page_number = request.GET.get('page', 1)
    
    try:
        milk_records = paginator.page(page_number)
    except:
        milk_records = paginator.page(1)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If AJAX request, return only the table content
        html = render_to_string(
            'farm_management/includes/milk_records_table.html',
            {'milk_records': milk_records}
        )
        return JsonResponse({
            'html': html,
            'has_next': milk_records.has_next(),
            'has_previous': milk_records.has_previous(),
            'current_page': milk_records.number,
            'total_pages': paginator.num_pages,
        })
    
    context = {
        'cow': cow,
        'milk_records': milk_records,
        'total_production': total_production,
        'avg_production': avg_production,
        'total_pages': paginator.num_pages,
        'current_page': milk_records.number,
    }
    return render(request, 'farm_management/cow_milk_history.html', context)

@login_required
def milk_production_list(request):
    farm = request.user.farm_set.first()
    records_list = MilkProduction.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')
    
    # Pagination
    paginator = Paginator(records_list, 2)  # Show 10 records per page
    page_number = request.GET.get('page', 1)
    
    try:
        records_list = paginator.page(page_number)
    except:
        records_list = paginator.page(1)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'farm_management/includes/milk_records_table_rows.html',
            {'records_list': records_list}
        )
        return JsonResponse({
            'html': html,
            'has_next': records_list.has_next(),
            'has_previous': records_list.has_previous(),
            'current_page': records_list.number,
            'total_pages': paginator.num_pages,
        })
    
    context = {
        'records_list': records_list,
        'total_pages': paginator.num_pages,
        'current_page': records_list.number,
        'has_previous': records_list.has_previous(),
        'has_next': records_list.has_next(),
        'previous_page_number': records_list.previous_page_number if records_list.has_previous() else 1,
        'next_page_number': records_list.next_page_number if records_list.has_next() else paginator.num_pages,
    }
    return render(request, 'farm_management/milk_production_list.html', context)

@login_required
def vet_record_list(request):
    farm = request.user.farm_set.first()
    records = VeterinaryRecord.objects.select_related('cow').filter(
        cow__farm=farm
    ).order_by('-date')
    return render(request, 'farm_management/vet_record_list.html', {'records': records})

@login_required
def cow_vet_history(request, tag_number):
    farm = request.user.farm_set.first()
    cow = get_object_or_404(Cow, farm=farm, tag_number=tag_number)
    vet_records = cow.vet_records.all().order_by('-date')
    
    # Calculate vet statistics
    total_cost = sum(record.cost for record in vet_records if record.cost is not None)
    records_by_type = {}
    for record in vet_records:
        records_by_type[record.record_type] = records_by_type.get(record.record_type, 0) + 1
    
    context = {
        'cow': cow,
        'vet_records': vet_records,
        'total_cost': total_cost,
        'records_by_type': records_by_type,
    }
    return render(request, 'farm_management/cow_vet_history.html', context)

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
    record_type = request.POST.get('type') or request.GET.get('type', 'morning')
    date = request.POST.get('date') or request.GET.get('date', timezone.now().date().isoformat())
    existing_record = None
    
    if request.method == 'POST':
        form = MilkProductionForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.recorded_by = request.user
            
            # Check for existing record
            existing_record = MilkProduction.objects.filter(
                cow=record.cow,
                date=record.date
            ).first()
            
            try:
                if existing_record:
                    # Update the existing record
                    if record_type == 'morning':
                        existing_record.morning_amount = form.cleaned_data['morning_amount']
                    else:
                        existing_record.evening_amount = form.cleaned_data['evening_amount']
                    
                    if form.cleaned_data.get('fat_content'):
                        existing_record.fat_content = form.cleaned_data['fat_content']
                    
                    if form.cleaned_data.get('notes'):
                        new_note = f"[{record_type.title()} Update] {form.cleaned_data['notes']}"
                        existing_record.notes = new_note if not existing_record.notes else f"{existing_record.notes}\n{new_note}"
                    
                    existing_record.save()
                else:
                    # Create new record
                    if record_type == 'morning':
                        record.morning_amount = form.cleaned_data['morning_amount']
                        record.evening_amount = None
                    else:
                        record.evening_amount = form.cleaned_data['evening_amount']
                        record.morning_amount = None
                    record.save()
                
                messages.success(request, f'{record_type.title()} milk production {"updated" if existing_record else "recorded"} successfully.')
                return redirect('farm_management:milk_production_list')
                
            except Exception as e:
                messages.error(request, f"Error saving record: {str(e)}")
    else:
        # GET request
        initial_data = {'date': date}
        if 'cow' in request.GET:
            cow = get_object_or_404(Cow, farm=farm, tag_number=request.GET['cow'])
            initial_data['cow'] = cow
            existing_record = MilkProduction.objects.filter(
                cow=cow,
                date=date
            ).first()
            if existing_record:
                initial_data.update({
                    'morning_amount': existing_record.morning_amount,
                    'evening_amount': existing_record.evening_amount,
                    'fat_content': existing_record.fat_content,
                    'notes': existing_record.notes
                })
        
        form = MilkProductionForm(initial=initial_data)
        form.fields['cow'].queryset = Cow.objects.filter(farm=farm)
        
        # Hide inappropriate field based on record type
        if record_type == 'morning':
            form.fields['evening_amount'].widget = forms.HiddenInput()
        else:
            form.fields['morning_amount'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'record_type': record_type,
        'date': date,
        'existing_record': existing_record
    }
    
    return render(request, 'farm_management/milk_production_form.html', context)

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
