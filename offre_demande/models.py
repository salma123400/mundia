from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from AUTH_APP.models import *

# Create your models here.
class DemandeDEmploi(models.Model):
    id_demande = models.AutoField(primary_key=True)
    date_soumission = models.DateTimeField()
    description = models.CharField(max_length=50)
    user = models.ForeignKey(Candidat, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.nom + ' ' + self.description

class Competence(models.Model):
    id_competence = models.AutoField(primary_key=True)
    nom_competence = models.CharField(max_length=50)
    def __str__(self):
        return self.nom_competence 

class OffreDEmploi(models.Model):
    id_offre = models.AutoField(primary_key=True)
    titre_poste = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    competence = models.CharField(max_length=50)
    date_publication_present = models.DateField()
    date_limite_candidature = models.DateField()
    salaire_propose = models.PositiveIntegerField()
    recruteur = models.ForeignKey(Recruteur, on_delete=models.CASCADE)
    def __str__(self):
        return self.recruteur.nom_recruteur + ' ' + self.titre_poste

class Diplome(models.Model):
    id_diplome = models.AutoField(primary_key=True)
    nom_diplome = models.CharField(max_length=50)

class Categorie(models.Model):
    id_catego = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    diplome = models.ForeignKey(Diplome, on_delete=models.CASCADE)

class Posseder(models.Model):
    TYPE_CHOICES = [
        ('Tres Bien','Tres Bien'),
        ('Bien','Bien'),
        ('Moyenne','Moyenne'),
        ('Debutant','Debutant')
    ]
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    id_competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    niveau_metrise = models.CharField(max_length=50)

    def __str__(self):
        return self.candidat.nom + ' ' + self.id_competence.nom_competence

    class Meta:
        unique_together = (('candidat', 'id_competence'))