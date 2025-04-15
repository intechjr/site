from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

