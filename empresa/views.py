from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import *
from .models import *

def home(request):
    # Busca a configuração da empresa (assume-se que só haverá uma empresa configurada)
    empresa = Empresa.objects.first()
    if not empresa:
        messages.error(request, "Nenhuma empresa foi configurada ainda.")
        return render(request, 'error.html', {'error': 'Empresa não configurada'}, status=500)
    elif not empresa.nome:
        messages.warning(request, "O nome da empresa não foi definido.")
        return render(request, 'error.html', {'error': 'Nome da Empresa não configurado'}, status=500)

    # Busca todas as abas relacionadas à empresa
    abas = Aba.objects.filter(empresa=empresa)

    # Busca todos os itens das abas
    aba_itens = {}
    for aba in abas:
        aba_itens[aba.nome] = AbaItem.objects.filter(aba=aba)

    # Busca as redes sociais da empresa
    redes_sociais = RedeSocial.objects.filter(empresa=empresa)

    whatsapp = redes_sociais.filter(nome='WhatsApp').first()

    # Renderiza o template com os dados
    return render(request, 'home.html', {
        'empresa': empresa,
        'abas': abas,
        'aba_itens': aba_itens,
        'redes_sociais': redes_sociais,
        'whatsapp': whatsapp,
        'contato': empresa.contato,
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

