from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PerfilUsuario, Usuario

class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    list_display = ['email', 'nickname', 'is_admin']
    search_fields = ['email', 'nickname']
    readonly_fields = ['id', 'date_joined', 'last_login']
    ordering = ['email']  # Use 'email' para ordenação

    # Ajuste os fieldsets para incluir os campos do seu modelo de usuário personalizado
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nickname',)}),
        ('Permissões', {'fields': ('is_admin', 'is_active')}),
    )
    # Ajuste o add_fieldsets para especificar os campos necessários ao criar um usuário através do admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2'),
        }),
    )
    filter_horizontal = []
    list_filter = ['is_admin']


# Classe ModelAdmin opcional para customização
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_nascimento', 'numero_registro')  # Campos que você quer mostrar na listagem
    search_fields = ('usuario__username', 'numero_registro')  # Campos pelos quais você quer permitir busca
    filter_horizontal = ('papeis',)  # Facilita a seleção de múltiplos papéis


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
