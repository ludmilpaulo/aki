from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail


##########################################################################
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


####################################################################################

from django.contrib.auth.models import AbstractUser, Group, Permission




def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_customer = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    # Provide unique related_name for groups and user_permissions
    # to avoid clashes with the auth.User model
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='shop_user_groups'  # unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='shop_user_permissions'  # unique related_name
    )

    def __str__(self):
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

####################################################################################

class ImageField(models.ImageField):
    def value_to_string(self, obj): # obj is Model instance, in this case, obj is 'Class'
        return obj.avatar.url # not return self.url


#######################################################################################




class Customer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='customer', verbose_name='usuário')
    avatar = models.ImageField(upload_to='customer/', blank=True)
    phone = models.CharField(max_length=500, blank=True, verbose_name='telefone')
    address = models.CharField(max_length=500, blank=True, verbose_name='Endereço')

    class Meta:
        verbose_name ='Cliente'
        verbose_name_plural ='Clientes'

    def __str__(self):
        return self.user.get_username()


class Driver(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='driver', verbose_name='Utilizador')
    avatar = models.ImageField(upload_to='driver/', blank=True)
    phone = models.CharField(max_length=500, blank=True, verbose_name='telefone')
    address = models.CharField(max_length=500, blank=True, verbose_name='Endereço')
    location = models.CharField(max_length=500, blank=True, verbose_name='localização')

    class Meta:
        verbose_name ='Motorista'
        verbose_name_plural ='Motoristas'


    def __str__(self):
        return self.user.get_username()

class ImageField(models.ImageField):
    def value_to_string(self, obj): # obj is Model instance, in this case, obj is 'Class'
        return obj.avatar.url # not return self.url


#######################################################################################
class ShopCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField(max_length=200, blank=True,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Shop category'
        verbose_name_plural = 'Shop categories'
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField(max_length=200, blank=True,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'
    def __str__(self):
        return self.name

    # Other fields and methods as needed...

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário', blank=True)
    shop_category = models.ForeignKey(ShopCategory, related_name='shops', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500, verbose_name='Nome da loja')
    phone = models.CharField(max_length=500, verbose_name='Telefone da loja')
    address = models.CharField(max_length=500, verbose_name='Endereço da loja')
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False, verbose_name='Logotipa loja')
    Shop_license = models.FileField(upload_to='vendor/license', blank=True, verbose_name='Licenca da loja')
    barnner = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name 

  



class Image(models.Model):
    image = models.ImageField(max_length=3000, default=None, blank=True, upload_to='product_images/')
    
    def __str__(self):
        return self.image.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=200)
    images = models.ManyToManyField(Image)  # Many-to-many relationship with Image model
    rating = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    description = models.TextField()
   

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title   

class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField(max_length=200, blank=True,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Service category'
        verbose_name_plural = 'Service categories'
    def __str__(self):
        return self.name
    
    
    
class ServiceImage(models.Model):
    image = models.ImageField(max_length=3000, default=None, blank=True, upload_to='product_images/')
    
    def __str__(self):
        return self.image.name
class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, related_name='service', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    images = models.ManyToManyField(ServiceImage)  # Many-to-many relationship with Image model
    rating = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    description = models.TextField()


    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'

    def __str__(self):
        return self.title
    
    
    


class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, related_name='requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"





