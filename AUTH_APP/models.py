from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Recruteur(models.Model):
    user = models.OneToOneField(CustomUser,unique=True ,on_delete=models.CASCADE )
    id_recruteur=models.AutoField(primary_key=True)
    TYPE_CHOICES = [
        ('Entreprise', 'Entreprise'),
        ('Individuel', 'Individuel'),
    ]
    type_recruteur = models.CharField(choices=TYPE_CHOICES, max_length=20)
    address = models.CharField(max_length=100)
    num_telephone = models.CharField(max_length=50)
    secteur_activite = models.CharField(max_length=50)
    nom_recruteur = models.CharField(max_length=50)
    presentation = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    motdepass = models.CharField(max_length=128)
    is_candidat = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.motdepass = make_password(self.motdepass)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_recruteur 

class Candidat(models.Model):
    user = models.OneToOneField(CustomUser ,unique=True, on_delete=models.CASCADE )
    id_candidat=models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    num_telephone = models.CharField(max_length=50)
    presentation = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    motdepass = models.CharField(max_length=128)
    is_candidat= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.motdepass = make_password(self.motdepass)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom + ' ' + self.prenom