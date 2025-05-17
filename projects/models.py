from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Projet(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    PRIORITY_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
        ('urgente', 'Urgente'),
    ]

    nom = models.CharField(max_length=200, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(null=True, blank=True, verbose_name='Date de fin')
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente', verbose_name='Statut')
    priorite = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='moyenne', verbose_name='Priorité')

    chef_de_projet = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projets_diriges', verbose_name='Chef de projet')
    membres = models.ManyToManyField(User, related_name='projets_participes', blank=True, verbose_name='Membres')

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')

    def _str_(self):
        return self.nom

    class Meta:
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
        ordering = ['-date_creation']

class CategorieProjet(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='categories', verbose_name='Projet')

    def _str_(self):
        return self.nom

    class Meta:
        verbose_name = 'Catégorie de projet'
        verbose_name_plural = 'Catégories de projets'
        ordering = ['nom']