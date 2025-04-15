from django.shortcuts import *

from django.views.generic import *
from .models import *
from .forms import *



def home(request):
    services = Service.objects.all()
    portfolio_items = Portfolio.objects.all()
    return render(request, 'base.html', {
        'services': services,
        'portfolio_items': portfolio_items
    })

