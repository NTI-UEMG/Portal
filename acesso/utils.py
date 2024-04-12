from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

def enviar_email_de_verificacao(request, user, token_verificacao):
    dominio_atual = get_current_site(request).domain
    link_verificacao = reverse('verificar_usuario', kwargs={'token_verificacao': token_verificacao})
    url_completa = 'http://{}{}'.format(dominio_atual, link_verificacao)
    
    assunto = 'Portal UEMG - Confirme o seu cadastro'
    mensagem = 'Obrigado por fazer do nosso portal! Por favor, clique no link a seguir para verificar seu e-mail e confirmar o seu cadastro: {}'.format(url_completa)
    email_de = 'milton.neto@uemg.br'
    email_para = [user.email]
    
    send_mail(assunto, mensagem, email_de, email_para)
