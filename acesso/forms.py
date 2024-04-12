from django import forms
from django.contrib.auth.forms import UserCreationForm
from acesso.models import PerfilUsuario, Usuario
from django.core.validators import RegexValidator

# Form para o Cadastro de novos usuários do sistema
class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Institucional')
    nickname = forms.CharField(required=True, label='Apelido')

    class Meta:
        model = Usuario
        fields = ('nickname', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@uemg.br'):
            raise forms.ValidationError("Por favor, utilize um email institucional da UEMG.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nickname']
        if commit:
            user.save()
        return user


# Validador de CPF usando expressão regular
cpf_validator = RegexValidator(regex="^\d{3}\.\d{3}\.\d{3}\-\d{2}$",
                               message="Digite o CPF no formato 000.000.000-00")
# Form para atualizar o perfil dos usuários do sistema
class PerfilUsuarioForm(forms.ModelForm):
    cpf = forms.CharField(validators=[cpf_validator], widget=forms.TextInput(attrs={
        'pattern': '\d{3}\.\d{3}\.\d{3}\-\d{2}',  # Formato 000.000.000-00
        'placeholder': '000.000.000-00'  # Placeholder para guiar o usuário
    }))
    
    class Meta:
        model = PerfilUsuario
        fields = ['nome', 'foto', 'data_nascimento', 'telefone', 'curso', 'rg', 'cpf']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),  # Facilita a entrada de datas
        }        

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        # Checa se o instance do formulário possui um CPF definido
        if self.instance and self.instance.cpf:
            cpf = self.instance.cpf
            # Aplica a formatação ao CPF
            cpf_formatado = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
            # Define o valor inicial do campo cpf no formulário com o cpf formatado
            self.fields['cpf'].initial = cpf_formatado
            