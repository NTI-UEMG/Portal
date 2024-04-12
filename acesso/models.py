import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from administrativo.models import Curso, Papel

class MeuGerenciadorDeUsuarios(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        user = self.create_user(email, nickname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True, validators=[RegexValidator(regex='^[\w\.-]+@uemg\.br$', message='O e-mail deve ser institucional da UEMG.')])
    nickname = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = MeuGerenciadorDeUsuarios()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class TokenVerificacao(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token para {self.usuario.nickname}"

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    #papel = models.ForeignKey(Papel, on_delete=models.SET_NULL, null=True)
    papeis = models.ManyToManyField(Papel, blank=True)  # Permite múltiplos papéis    
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    numero_registro = models.CharField(max_length=50, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    verificado = models.BooleanField(default=False)
