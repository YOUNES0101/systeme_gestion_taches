from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from projects.models import Projet  # Correction de l'import (projects au lieu de projets)

class Tache(models.Model):
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
        ('critique', 'Critique'),
    ]

    STATUT_CHOICES = [
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('en_retard', 'En retard'),
    ]

    titre = models.CharField(max_length=255, verbose_name='Titre')
    description = models.TextField(blank=True, verbose_name='Description')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches', verbose_name='Projet')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='taches_assignees', verbose_name='Assigné à')

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    date_echeance = models.DateField(null=True, blank=True, verbose_name='Date d\'échéance')

    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne', verbose_name='Priorité')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_faire', verbose_name='Statut')

    temps_estime = models.PositiveIntegerField(null=True, blank=True, verbose_name='Temps estimé (heures)')
    temps_passe = models.PositiveIntegerField(null=True, blank=True, verbose_name='Temps passé (heures)')

    def _str_(self):
        return f"{self.titre} ({self.projet.nom})"

    class Meta:
        verbose_name = 'Tâche'
        verbose_name_plural = 'Tâches'
        ordering = ['-date_creation']

class Commentaire(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='commentaires', verbose_name='Tâche')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentaires_tache', verbose_name='Auteur')
    contenu = models.TextField(verbose_name='Contenu')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def _str_(self):
        return f"Commentaire de {self.auteur.username} sur {self.tache.titre}"

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['-date_creation']