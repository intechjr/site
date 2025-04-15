from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import *
from .models import *

def home(request):
    services = Service.objects.all()
    portfolio_items = Portfolio.objects.all()
    return render(request, 'base.html', {
        'services': services,
        'portfolio_items': portfolio_items
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('nome', '')
        email = request.POST.get('email', '')
        message = request.POST.get('mensagem', '')
        
        # Montar o corpo do email
        email_body = f"Nome: {name}\nEmail: {email}\n\nMensagem:\n{message}"
        
        try:
            # Enviar o email
            send_mail(
                subject=f'Contato do site - {name}',
                message=email_body,
                from_email='intechjr@gmail.com',
                recipient_list=['intechjr@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Mensagem enviada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao enviar mensagem: {str(e)}')
        
        return redirect('home')
    
    return redirect('home')

