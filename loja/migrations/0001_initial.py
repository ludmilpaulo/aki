# Generated by Django 4.2.3 on 2023-08-25 15:29

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_index=True, max_length=200, verbose_name='Nome')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='cliente_avatars/', verbose_name='Avatar')),
                ('telefone', models.CharField(blank=True, max_length=500, verbose_name='Telefone')),
                ('endereco', models.CharField(blank=True, max_length=500, verbose_name='Endereço')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_fornecedor', models.CharField(max_length=50, verbose_name='Nome do Fornecedor')),
                ('telefone', models.CharField(max_length=500, verbose_name='Telefone do Fornecedor')),
                ('endereco', models.CharField(max_length=500, verbose_name='Endereço do Fornecedor')),
                ('logo', models.ImageField(upload_to='logo_fornecedor/', verbose_name='Logotipo do Fornecedor')),
                ('licenca', models.ImageField(upload_to='licencas_fornecedor/', verbose_name='Licença do Fornecedor')),
                ('aprovado', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')),
                ('modificado_em', models.DateTimeField(auto_now=True, verbose_name='Modificado Em')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('e_cliente', models.BooleanField(default=False, verbose_name='É Cliente')),
                ('e_motorista', models.BooleanField(default=False, verbose_name='É Motorista')),
                ('e_fornecedor', models.BooleanField(default=False, verbose_name='É Fornecedor')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='usuario_groups', related_query_name='usuario_group', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='usuario_permissions', related_query_name='usuario_permission', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=500, verbose_name='Nome')),
                ('descricao_curta', models.CharField(max_length=500, verbose_name='Descrição Curta')),
                ('imagem', models.ImageField(upload_to='imagens_refeicao/', verbose_name='Imagem da Refeição')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
                ('slug', models.SlugField(blank=True, max_length=500, unique=True, verbose_name='Slug')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')),
                ('modificado_em', models.DateTimeField(auto_now=True, verbose_name='Modificado Em')),
                ('disponivel', models.BooleanField(default=True, verbose_name='Disponível')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refeicoes', to='loja.categoria', verbose_name='Categoria')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.fornecedor', verbose_name='Fornecedor')),
            ],
            options={
                'verbose_name': 'Refeição',
                'verbose_name_plural': 'Refeições',
                'ordering': ('-criado_em',),
                'index_together': {('id', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco_entrega', models.CharField(max_length=500, verbose_name='Endereço de Entrega')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('status_pedido', models.CharField(choices=[('Pendente', 'Pendente'), ('Em Processamento', 'Em Processamento'), ('A Caminho', 'A Caminho'), ('Entregue', 'Entregue'), ('Cancelado', 'Cancelado')], default='Pendente', max_length=200, verbose_name='Status do Pedido')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')),
                ('modificado_em', models.DateTimeField(auto_now=True, verbose_name='Modificado Em')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.cliente', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ('-criado_em',),
            },
        ),
        migrations.CreateModel(
            name='Motorista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='motorista_avatars/', verbose_name='Avatar')),
                ('telefone', models.CharField(blank=True, max_length=500, verbose_name='Telefone')),
                ('endereco', models.CharField(blank=True, max_length=500, verbose_name='Endereço')),
                ('localizacao_atual', models.CharField(blank=True, max_length=500, verbose_name='Localização Atual')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='motorista', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Motorista',
                'verbose_name_plural': 'Motoristas',
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
                ('quantidade', models.PositiveIntegerField(default=1, verbose_name='Quantidade')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='loja.pedido', verbose_name='Pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido', to='loja.produto', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item do Pedido',
                'verbose_name_plural': 'Itens do Pedido',
            },
        ),
        migrations.CreateModel(
            name='HorarioFuncionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.IntegerField(choices=[(1, 'Segunda-feira'), (2, 'Terça-feira'), (3, 'Quarta-feira'), (4, 'Quinta-feira'), (5, 'Sexta-feira'), (6, 'Sábado'), (7, 'Domingo')], verbose_name='Dia')),
                ('hora_inicial', models.CharField(choices=[('12:00 AM', '12:00 AM'), ('12:30 AM', '12:30 AM'), ('01:00 AM', '01:00 AM'), ('01:30 AM', '01:30 AM'), ('02:00 AM', '02:00 AM'), ('02:30 AM', '02:30 AM'), ('03:00 AM', '03:00 AM'), ('03:30 AM', '03:30 AM'), ('04:00 AM', '04:00 AM'), ('04:30 AM', '04:30 AM'), ('05:00 AM', '05:00 AM'), ('05:30 AM', '05:30 AM'), ('06:00 AM', '06:00 AM'), ('06:30 AM', '06:30 AM'), ('07:00 AM', '07:00 AM'), ('07:30 AM', '07:30 AM'), ('08:00 AM', '08:00 AM'), ('08:30 AM', '08:30 AM'), ('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'), ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'), ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('01:00 PM', '01:00 PM'), ('01:30 PM', '01:30 PM'), ('02:00 PM', '02:00 PM'), ('02:30 PM', '02:30 PM'), ('03:00 PM', '03:00 PM'), ('03:30 PM', '03:30 PM'), ('04:00 PM', '04:00 PM'), ('04:30 PM', '04:30 PM'), ('05:00 PM', '05:00 PM'), ('05:30 PM', '05:30 PM'), ('06:00 PM', '06:00 PM'), ('06:30 PM', '06:30 PM'), ('07:00 PM', '07:00 PM'), ('07:30 PM', '07:30 PM'), ('08:00 PM', '08:00 PM'), ('08:30 PM', '08:30 PM'), ('09:00 PM', '09:00 PM'), ('09:30 PM', '09:30 PM'), ('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'), ('11:00 PM', '11:00 PM'), ('11:30 PM', '11:30 PM')], max_length=10, verbose_name='Hora de Início')),
                ('hora_final', models.CharField(choices=[('12:00 AM', '12:00 AM'), ('12:30 AM', '12:30 AM'), ('01:00 AM', '01:00 AM'), ('01:30 AM', '01:30 AM'), ('02:00 AM', '02:00 AM'), ('02:30 AM', '02:30 AM'), ('03:00 AM', '03:00 AM'), ('03:30 AM', '03:30 AM'), ('04:00 AM', '04:00 AM'), ('04:30 AM', '04:30 AM'), ('05:00 AM', '05:00 AM'), ('05:30 AM', '05:30 AM'), ('06:00 AM', '06:00 AM'), ('06:30 AM', '06:30 AM'), ('07:00 AM', '07:00 AM'), ('07:30 AM', '07:30 AM'), ('08:00 AM', '08:00 AM'), ('08:30 AM', '08:30 AM'), ('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'), ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'), ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('01:00 PM', '01:00 PM'), ('01:30 PM', '01:30 PM'), ('02:00 PM', '02:00 PM'), ('02:30 PM', '02:30 PM'), ('03:00 PM', '03:00 PM'), ('03:30 PM', '03:30 PM'), ('04:00 PM', '04:00 PM'), ('04:30 PM', '04:30 PM'), ('05:00 PM', '05:00 PM'), ('05:30 PM', '05:30 PM'), ('06:00 PM', '06:00 PM'), ('06:30 PM', '06:30 PM'), ('07:00 PM', '07:00 PM'), ('07:30 PM', '07:30 PM'), ('08:00 PM', '08:00 PM'), ('08:30 PM', '08:30 PM'), ('09:00 PM', '09:00 PM'), ('09:30 PM', '09:30 PM'), ('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'), ('11:00 PM', '11:00 PM'), ('11:30 PM', '11:30 PM')], max_length=10, verbose_name='Hora de Término')),
                ('fechar', models.BooleanField(default=False, verbose_name='Fechado')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.fornecedor', verbose_name='Fornecedor')),
            ],
            options={
                'verbose_name': 'Horário de Funcionamento',
                'verbose_name_plural': 'Horários de Funcionamento',
                'ordering': ('dia', '-hora_inicial'),
                'unique_together': {('fornecedor', 'dia', 'hora_inicial', 'hora_final')},
            },
        ),
    ]
