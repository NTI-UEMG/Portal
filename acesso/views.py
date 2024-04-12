from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

from acesso.models import PerfilUsuario, TokenVerificacao
from acesso.utils import enviar_email_de_verificacao
from .forms import CadastroUsuarioForm, PerfilUsuarioForm
from administrativo.models import Curso, Papel

def index(request):
    cursos = Curso.objects.all()  # Ou qualquer filtro que você deseja aplicar
    return render(request, 'index.html', {'cursos': cursos})

#def index(request):
#    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se o e-mail termina com @uemg.br
        if not username.endswith('@uemg.br'):
            messages.error(request, 'Por favor, utilize seu e-mail institucional da UEMG.')
            return render(request, 'acesso/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
            
            if perfil.verificado:
                login(request, user)
                return redirect('index')  # Substitua 'index' pelo nome da sua URL de destino após o login
            else:
                messages.error(request, 'Usuário ainda não verificado!')
                return render(request, 'acesso/login.html')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'acesso/login.html')

    return render(request, 'acesso/login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            if user and user.pk:
                # Gerar e salvar o token de verificação
                token = TokenVerificacao.objects.create(usuario=user)
                
                # Enviar e-mail de verificação
                enviar_email_de_verificacao(request, user, token.token)
                    
                return redirect('login')  # Redireciona para a página de login após o cadastro bem-sucedido
            else:
                messages.error(request, 'Ocorreu um erro na criação do usuário.')
                return render(request, 'acesso/login.html')
    else:
        form = CadastroUsuarioForm()
        
    return render(request, 'acesso/cadastro.html', {'form': form})

def verificar_usuario(request, token_verificacao):
    try:
        token = get_object_or_404(TokenVerificacao, token=token_verificacao)
        user = token.usuario
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
        
        # Marcar o usuário como verificado
        perfil.verificado = True
        
        # Verificar se o usuário é um aluno com base no e-mail
        if user.email.startswith('discente'):
            # Buscar o papel "Aluno" na tabela Papel
            papel_aluno = Papel.objects.get(descricao="Aluno")

            # Adicionar o papel "Aluno" ao perfil do usuário
            perfil.papeis.add(papel_aluno)    
            
            # Extrair a matrícula do e-mail. Ajuste a lógica conforme o formato exato do e-mail.
            matricula = user.email.split('@')[0].replace('discente', '')
            perfil.numero_registro = matricula
        
        perfil.save()
        
        # Não esqueça de invalidar ou deletar o token após a verificação para evitar reuso
        token.delete()

        messages.success(request, 'Usuário verificado com sucesso!')
        # Redireciona para a página de atualização do perfil
        return redirect('preencher_perfil_view')  
    
    except TokenVerificacao.DoesNotExist:
        messages.error(request, 'Ocorreu um erro na verificação do usuário.')
        return redirect('login')

def perfil_view(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redireciona para home
        else:
            messages.error(request, 'Ocorreu um erro na atualização do perfil do usuário.')
            for field, errors in form.errors.items():
                for error in errors:
                    # Cria uma mensagem de erro para cada erro de validação
                    messages.error(request, f"Erro no campo {field}: {error}")
            return redirect('index')
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario)
        
    return render(request, 'acesso/perfil.html', {'form': form})

# Para redirecionar o usuário para a página inicial (home, index.html) após salvar as alterações no perfil, 
# você deve ajustar a view de atualização do perfil.

