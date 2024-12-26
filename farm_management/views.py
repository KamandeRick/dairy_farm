from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
<<<<<<< HEAD
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
=======
from django.contrib.auth.forms import UserCreationForm
>>>>>>> 8d55bc62081881fbf1501bb381c39602f20b88f8
from .models import Farm, Cow, MilkProduction, VeterinaryRecord
from .forms import CowForm, MilkProductionForm, VeterinaryRecordForm
from .mixins import FarmUserMixin, FarmManagerMixin, FarmOwnerMixin

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
<<<<<<< HEAD
=======
            # Create a farm for the new user
>>>>>>> 8d55bc62081881fbf1501bb381c39602f20b88f8
            farm = Farm.objects.create(
                name=f"{user.username}'s Farm",
                owner=user
            )
<<<<<<< HEAD
            owner_group, created = Group.objects.get(name='Farm Owner')

            content_type = ContentType.objects.get_for_model(Cow)
            permissions = Permission.objects.filter(content_type=content_type)
            owner_group.permissions.set(permissions)

            user.groups.add(owner_group)
=======
            # Add user to Farm Owner group
            owner_group = Group.objects.get(name='Farm Owner')
            user.groups.add(owner_group)


>>>>>>> 8d55bc62081881fbf1501bb381c39602f20b88f8
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class DashboardView(LoginRequiredMixin, FarmUserMixin, DetailView):
    model = Farm
    template_name = 'farm_management/dashboard.html'
    context_object_name = 'farm'

    def get_object(self):
        return get_object_or_404(Farm, owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = self.get_object()
        context.update({
            'total_cows': Cow.objects.filter(farm=farm).count(),
            'active_cows': Cow.objects.filter(farm=farm, status='ACTIVE').count(),
            'latest_milk_records': MilkProduction.objects.select_related('cow').filter(
                cow__farm=farm
            ).order_by('-date')[:5],
            'recent_vet_records': VeterinaryRecord.objects.select_related('cow').filter(
                cow__farm=farm
            ).order_by('-date')[:5],
        })
        return context

class CowListView(LoginRequiredMixin, FarmUserMixin, ListView):
    model = Cow
    template_name = 'farm_management/cow_list.html'
    context_object_name = 'cows'

    def get_queryset(self):
        return Cow.objects.filter(farm__owner=self.request.user)

class CowDetailView(LoginRequiredMixin, FarmUserMixin, DetailView):
    model = Cow
    template_name = 'farm_management/cow_detail.html'
    context_object_name = 'cow'
    slug_field = 'tag_number'
    slug_url_kwarg = 'tag_number'

    def get_queryset(self):
        return Cow.objects.filter(farm__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cow = self.get_object()
        context.update({
            'milk_records': cow.milk_records.order_by('-date')[:10],
            'vet_records': cow.vet_records.order_by('-date')[:10],
        })
        return context

class CowCreateView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, CreateView):
    model = Cow
    form_class = CowForm
    template_name = 'farm_management/cow_form.html'
    permission_required = 'farm_management.add_cow'
    success_url = reverse_lazy('farm_management:cow_list')

    def form_valid(self, form):
        form.instance.farm = self.request.user.farm_set.first()
        return super().form_valid(form)

class MilkProductionListView(LoginRequiredMixin, FarmUserMixin, ListView):
    model = MilkProduction
    template_name = 'farm_management/milk_production_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return MilkProduction.objects.select_related('cow').filter(
            cow__farm__owner=self.request.user
        ).order_by('-date')

class MilkProductionCreateView(LoginRequiredMixin, FarmUserMixin, PermissionRequiredMixin, CreateView):
    model = MilkProduction
    form_class = MilkProductionForm
    template_name = 'farm_management/milk_production_form.html'
    permission_required = 'farm_management.add_milkproduction'
    success_url = reverse_lazy('farm_management:milk_production_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cow'].queryset = Cow.objects.filter(
            farm__owner=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        return super().form_valid(form)

class MilkProductionUpdateView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, UpdateView):
    model = MilkProduction
    form_class = MilkProductionForm
    template_name = 'farm_management/milk_production_form.html'
    permission_required = 'farm_management.change_milkproduction'
    success_url = reverse_lazy('farm_management:milk_production_list')

    def get_queryset(self):
        return MilkProduction.objects.filter(cow__farm__owner=self.request.user)

class MilkProductionDeleteView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, DeleteView):
    model = MilkProduction
    template_name = 'farm_management/milk_production_confirm_delete.html'
    permission_required = 'farm_management.delete_milkproduction'
    success_url = reverse_lazy('farm_management:milk_production_list')

    def get_queryset(self):
        return MilkProduction.objects.filter(cow__farm__owner=self.request.user)

class VetRecordListView(LoginRequiredMixin, FarmUserMixin, ListView):
    model = VeterinaryRecord
    template_name = 'farm_management/vet_record_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return VeterinaryRecord.objects.select_related('cow').filter(
            cow__farm__owner=self.request.user
        ).order_by('-date')

class VetRecordCreateView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, CreateView):
    model = VeterinaryRecord
    form_class = VeterinaryRecordForm
    template_name = 'farm_management/vet_record_form.html'
    permission_required = 'farm_management.add_veterinaryrecord'
    success_url = reverse_lazy('farm_management:vet_record_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cow'].queryset = Cow.objects.filter(
            farm__owner=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        return super().form_valid(form)

class VetRecordUpdateView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, UpdateView):
    model = VeterinaryRecord
    form_class = VeterinaryRecordForm
    template_name = 'farm_management/vet_record_form.html'
    permission_required = 'farm_management.change_veterinaryrecord'
    success_url = reverse_lazy('farm_management:vet_record_list')

    def get_queryset(self):
        return VeterinaryRecord.objects.filter(cow__farm__owner=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cow'].queryset = Cow.objects.filter(
            farm__owner=self.request.user
        )
        return form

class VetRecordDeleteView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, DeleteView):
    model = VeterinaryRecord
    template_name = 'farm_management/vet_record_confirm_delete.html'
    permission_required = 'farm_management.delete_veterinaryrecord'
    success_url = reverse_lazy('farm_management:vet_record_list')

    def get_queryset(self):
        return VeterinaryRecord.objects.filter(cow__farm__owner=self.request.user)

class CowUpdateView(LoginRequiredMixin, FarmManagerMixin, PermissionRequiredMixin, UpdateView):
    model = Cow
    form_class = CowForm
    template_name = 'farm_management/cow_form.html'
    permission_required = 'farm_management.change_cow'
    success_url = reverse_lazy('farm_management:cow_list')
    
    def get_queryset(self):
        return Cow.objects.filter(farm__owner=self.request.user)

class CowDeleteView(LoginRequiredMixin, FarmOwnerMixin, PermissionRequiredMixin, DeleteView):
    model = Cow
    template_name = 'farm_management/cow_confirm_delete.html'
    permission_required = 'farm_management.delete_cow'
    success_url = reverse_lazy('farm_management:cow_list')

    def get_queryset(self):
        return Cow.objects.filter(farm__owner=self.request.user)

class FarmUpdateView(LoginRequiredMixin, FarmOwnerMixin, UpdateView):
    model = Farm
    fields = ['name', 'address', 'phone']
    template_name = 'farm_management/farm_form.html'
    success_url = reverse_lazy('farm_management:dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(Farm, owner=self.request.user)
