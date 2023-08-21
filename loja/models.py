from django.db import models

from datetime import datetime, time, date
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail

from django.contrib.auth.models import AbstractUser, Group, Permission, User

from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    e_cliente = models.BooleanField(default=False, verbose_name='É Cliente')
    e_motorista = models.BooleanField(default=False, verbose_name='É Motorista')
    e_fornecedor = models.BooleanField(default=False, verbose_name='É Fornecedor')

    # Explicitly define groups and user_permissions without using translations
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='usuario_groups',
        related_query_name='usuario_group',
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        )
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='usuario_permissions',
        related_query_name='usuario_permission',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username


# Cria um token de autenticação sempre que um usuário é criado
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_token_autenticacao(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Modelo para categorias de refeições
class Categoria(models.Model):
    nome = models.CharField(max_length=200, db_index=True, verbose_name='Nome')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ('nome',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nome



class Fornecedor(models.Model):
    usuario = models.OneToOneField(User, related_name='fornecedor', on_delete=models.CASCADE)
    nome_fornecedor = models.CharField(max_length=50, verbose_name='Nome do Fornecedor')
    telefone = models.CharField(max_length=500, verbose_name='Telefone do Fornecedor')
    endereco = models.CharField(max_length=500, verbose_name='Endereço do Fornecedor')
    logo = models.ImageField(upload_to='logo_fornecedor/', blank=False, verbose_name='Logotipo do Fornecedor')
    licenca = models.ImageField(upload_to='licencas_fornecedor/', verbose_name='Licença do Fornecedor')
    aprovado = models.BooleanField(default=False, verbose_name='Aprovado')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')
    modificado_em = models.DateTimeField(auto_now=True, verbose_name='Modificado Em')

    def __str__(self):
        return self.nome_fornecedor

    def save(self, *args, **kwargs):
        # If the object has a primary key, it's an update not a new creation
        if self.pk:
            original = Fornecedor.objects.get(pk=self.pk)
            # Check if the 'aprovado' field has changed
            if original.aprovado != self.aprovado:
                self.send_approval_email()
        else:
            # This means it's a new sign-up
            self.send_signup_email()

        super(Fornecedor, self).save(*args, **kwargs)

    def send_signup_email(self):
        """Send a sign-up confirmation email."""
        subject = 'Bem-vindo ao nossa plataforma!'
        message = 'Obrigado por se inscrever. Estamos revisando sua inscrição e entraremos em contato em breve!'
        email_from = 'contact@ludmilpaulo.com'
        send_mail(subject, message, email_from, [self.usuario.email])

    def send_approval_email(self):
        """Send an email based on the 'aprovado' status."""
        subject = 'Seu status na plataforma'
        if self.aprovado:
            message = 'Parabéns! Seu negócio foi aprovado e agora está ativo em nossa plataforma.'
        else:
            message = 'Lamentamos! Você não está apto para publicar seu cardápio em nossa plataforma.'
        email_from = 'contact@ludmilpaulo.com'
        send_mail(subject, message, email_from, [self.usuario.email])


    def esta_aberto(self):
        hoje = date.today()
        dia_atual = hoje.isoweekday()
        horarios_atuais = HorarioFuncionamento.objects.filter(fornecedor=self, dia=dia_atual)
        agora = datetime.now().time()

        for horario in horarios_atuais:
            if not horario.fechar:
                inicio = datetime.strptime(horario.hora_inicial, "%I:%M %p").time()
                fim = datetime.strptime(horario.hora_final, "%I:%M %p").time()
                if inicio <= agora <= fim:
                    return True
        return False


DIAS = [
    (1, "Segunda-feira"),
    (2, "Terça-feira"),
    (3, "Quarta-feira"),
    (4, "Quinta-feira"),
    (5, "Sexta-feira"),
    (6, "Sábado"),
    (7, "Domingo"),
]

HORARIO_24_HORAS = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]

class HorarioFuncionamento(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name='Fornecedor')
    dia = models.IntegerField(choices=DIAS, verbose_name='Dia')
    hora_inicial = models.CharField(choices=HORARIO_24_HORAS, max_length=10, verbose_name='Hora de Início')
    hora_final = models.CharField(choices=HORARIO_24_HORAS, max_length=10, verbose_name='Hora de Término')
    fechar = models.BooleanField(default=False, verbose_name='Fechado')

    class Meta:
        ordering = ('dia', '-hora_inicial')
        unique_together = ('fornecedor', 'dia', 'hora_inicial', 'hora_final')
        verbose_name = 'Horário de Funcionamento'
        verbose_name_plural = 'Horários de Funcionamento'

    def __str__(self):
        return f"{self.get_dia_display()} - {self.hora_inicial} até {self.hora_final}"

# Modelo para clientes
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente', verbose_name='Usuário')
    avatar = models.ImageField(upload_to='cliente_avatars/', blank=True, verbose_name='Avatar')
    telefone = models.CharField(max_length=500, blank=True, verbose_name='Telefone')
    endereco = models.CharField(max_length=500, blank=True, verbose_name='Endereço')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.usuario.username

# Modelo para motoristas
class Motorista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='motorista', verbose_name='Usuário')
    avatar = models.ImageField(upload_to='motorista_avatars/', blank=True, verbose_name='Avatar')
    telefone = models.CharField(max_length=500, blank=True, verbose_name='Telefone')
    endereco = models.CharField(max_length=500, blank=True, verbose_name='Endereço')
    localizacao_atual = models.CharField(max_length=500, blank=True, verbose_name='Localização Atual')

    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'

    def __str__(self):
        return self.usuario.username

# Modelo para refeições
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='refeicoes', on_delete=models.CASCADE, verbose_name='Categoria')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name='Fornecedor')
    nome = models.CharField(max_length=500, verbose_name='Nome')
    descricao_curta = models.CharField(max_length=500, verbose_name='Descrição Curta')
    imagem = models.ImageField(upload_to='imagens_refeicao/', blank=False, verbose_name='Imagem da Refeição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    slug = models.SlugField(max_length=500, db_index=True, unique=True, verbose_name='Slug')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')
    modificado_em = models.DateTimeField(auto_now=True, verbose_name='Modificado Em')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')

    class Meta:
        ordering = ('-criado_em',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Refeição'
        verbose_name_plural = 'Refeições'

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    endereco_entrega = models.CharField(max_length=500, verbose_name='Endereço de Entrega')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    status_pedido = models.CharField(max_length=200, choices=[
        ('Pendente', 'Pendente'),
        ('Em Processamento', 'Em Processamento'),
        ('A Caminho', 'A Caminho'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ], default='Pendente', verbose_name='Status do Pedido')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')
    modificado_em = models.DateTimeField(auto_now=True, verbose_name='Modificado Em')

    class Meta:
        ordering = ('-criado_em',)
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido #{self.id}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE, verbose_name='Pedido')
    produto = models.ForeignKey(Produto, related_name='itens_pedido', on_delete=models.CASCADE, verbose_name='Produto')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    quantidade = models.PositiveIntegerField(default=1, verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f"{self.id} - {self.refeicao.nome} - {self.quantidade}"

