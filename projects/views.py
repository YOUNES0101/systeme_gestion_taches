from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Projet, CategorieProjet
from tasks.models import Tache
from django.contrib.auth.models import User

# Create your views here.

@login_required
def project_list(request):
    """Affiche la liste des projets"""
    # Projets dirigés par l'utilisateur
    projets_diriges = Projet.objects.filter(chef_de_projet=request.user)
    
    # Projets auxquels l'utilisateur participe
    projets_participes = Projet.objects.filter(membres=request.user).exclude(chef_de_projet=request.user)
    
    context = {
        'projets_diriges': projets_diriges,
        'projets_participes': projets_participes,
    }
    
    return render(request, 'project_list.html', context)

@login_required
def project_detail(request, projet_id):
    """Affiche les détails d'un projet spécifique"""
    projet = get_object_or_404(Projet, id=projet_id)
    
    # Vérifier que l'utilisateur a accès à ce projet
    if request.user != projet.chef_de_projet and request.user not in projet.membres.all():
        messages.error(request, "Vous n'avez pas accès à ce projet.")
        return redirect('project_list')
    
    # Compter les tâches par statut
    taches_en_cours = Tache.objects.filter(projet=projet, statut='en_cours').count()
    taches_terminees = Tache.objects.filter(projet=projet, statut='terminee').count()
    taches_en_retard = Tache.objects.filter(projet=projet, statut='en_retard').count()
    
    context = {
        'projet': projet,
        'taches_en_cours': taches_en_cours,
        'taches_terminees': taches_terminees,
        'taches_en_retard': taches_en_retard,
    }
    
    return render(request, 'project.html', context)

@login_required
def add_project(request):
    """Ajouter un nouveau projet"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin') or None
        statut = request.POST.get('statut')
        priorite = request.POST.get('priorite')
        
        if not nom or not date_debut:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('add_project')
        
        # Créer le projet
        projet = Projet.objects.create(
            nom=nom,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
            statut=statut,
            priorite=priorite,
            chef_de_projet=request.user
        )
        
        # Ajouter les membres sélectionnés
        membres_ids = request.POST.getlist('membres')
        if membres_ids:
            membres = User.objects.filter(id__in=membres_ids)
            projet.membres.add(*membres)
        
        messages.success(request, f"Le projet '{nom}' a été créé avec succès.")
        return redirect('project_detail', projet_id=projet.id)
    
    # Pour le formulaire GET
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'add_project.html', {'users': users})

@login_required
def edit_project(request, projet_id):
    """Modifier un projet existant"""
    projet = get_object_or_404(Projet, id=projet_id)
    
    # Vérifier que l'utilisateur est le chef de projet
    if request.user != projet.chef_de_projet:
        messages.error(request, "Seul le chef de projet peut modifier ce projet.")
        return redirect('project_detail', projet_id=projet.id)
    
    if request.method == 'POST':
        projet.nom = request.POST.get('nom')
        projet.description = request.POST.get('description')
        projet.date_debut = request.POST.get('date_debut')
        projet.date_fin = request.POST.get('date_fin') or None
        projet.statut = request.POST.get('statut')
        projet.priorite = request.POST.get('priorite')
        
        # Mettre à jour les membres
        membres_ids = request.POST.getlist('membres')
        projet.membres.clear()
        if membres_ids:
            membres = User.objects.filter(id__in=membres_ids)
            projet.membres.add(*membres)
        
        projet.save()
        messages.success(request, f"Le projet '{projet.nom}' a été mis à jour avec succès.")
        return redirect('project_detail', projet_id=projet.id)
    
    # Pour le formulaire GET
    users = User.objects.exclude(id=request.user.id)
    context = {
        'projet': projet,
        'users': users,
        'membres_actuels': [membre.id for membre in projet.membres.all()]
    }
    return render(request, 'edit_project.html', context)

@login_required
def add_task(request, projet_id):
    """Ajouter une tâche à un projet"""
    projet = get_object_or_404(Projet, id=projet_id)
    
    # Vérifier que l'utilisateur a accès à ce projet
    if request.user != projet.chef_de_projet and request.user not in projet.membres.all():
        messages.error(request, "Vous n'avez pas accès à ce projet.")
        return redirect('project_list')
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        priorite = request.POST.get('priorite')
        statut = request.POST.get('statut')
        date_echeance = request.POST.get('date_echeance') or None
        temps_estime = request.POST.get('temps_estime') or None
        assignee_id = request.POST.get('assignee')
        
        if not titre:
            messages.error(request, "Le titre de la tâche est obligatoire.")
            return redirect('project_detail', projet_id=projet.id)
        
        # Créer la tâche
        tache = Tache(
            titre=titre,
            description=description,
            projet=projet,
            priorite=priorite,
            statut=statut,
            date_echeance=date_echeance,
            temps_estime=temps_estime
        )
        
        # Assigner la tâche si un utilisateur est sélectionné
        if assignee_id:
            assignee = get_object_or_404(User, id=assignee_id)
            tache.assignee = assignee
        
        tache.save()
        messages.success(request, f"La tâche '{titre}' a été ajoutée au projet.")
        
        return redirect('project_detail', projet_id=projet.id)
    
    # Cette vue est généralement appelée via AJAX, donc pas de rendu GET
    return redirect('project_detail', projet_id=projet.id)
