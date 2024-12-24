from django.shortcuts import render

# Create your views here.
def index(request):
    """The home page for Farm Management"""
    return render(request, 'farm_management/index.html')
