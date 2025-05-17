from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Tache, Commentaire
from projects.models import Projet
from django.contrib.auth.models import User

# Create your views here.

@login_required
def task_list(request):
    """Affiche la liste des tâches de l'utilisateur"""
    # Tâches assignées à l'utilisateur
    taches_assignees = Tache.objects.filter(assignee=request.user)
    
    # Tâches des projets dirigés par l'utilisateur
    projets_diriges = Projet.objects.filter(chef_de_projet=request.user)
    taches_projets_diriges = Tache.objects.filter(projet__in=projets_diriges).exclude(assignee=request.user)
    
    # Tâches des projets auxquels l'utilisateur participe
    projets_participes = Projet.objects.filter(membres=request.user)
    taches_projets_participes = Tache.objects.filter(projet__in=projets_participes).exclude(assignee=request.user)
    
    context = {
        'taches_assignees': taches_assignees,
        'taches_projets_diriges': taches_projets_diriges,
        'taches_projets_participes': taches_projets_participes,
    }
    
    return render(request, 'task_list.html', context)

@login_required
def task_detail(request, tache_id):
    """Affiche les détails d'une tâche spécifique"""
    tache = get_object_or_404(Tache, id=tache_id)
    
    # Vérifier que l'utilisateur a accès à cette tâche
    projet = tache.projet
    if request.user != projet.chef_de_projet and request.user not in projet.membres.all() and request.user != tache.assignee:
        messages.error(request, "Vous n'avez pas accès à cette tâche.")
        return redirect('task_list')
    
    # Récupérer les commentaires
    commentaires = tache.commentaires.all().order_by('-date_creation')
    
    # Traitement du formulaire de commentaire
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Commentaire.objects.create(
                tache=tache,
                auteur=request.user,
                contenu=contenu
            )
            messages.success(request, "Votre commentaire a été ajouté.")
            return redirect('task_detail', tache_id=tache.id)
    
    context = {
        'tache': tache,
        'commentaires': commentaires,
    }
    
    return render(request, 'task_detail.html', context)

@login_required
def edit_task(request, tache_id):
    """Modifier une tâche existante"""
    tache = get_object_or_404(Tache, id=tache_id)
    projet = tache.projet
    
    # Vérifier que l'utilisateur a le droit de modifier cette tâche
    if request.user != projet.chef_de_projet and request.user != tache.assignee:
        messages.error(request, "Vous n'avez pas l'autorisation de modifier cette tâche.")
        return redirect('task_detail', tache_id=tache.id)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        priorite = request.POST.get('priorite')
        statut = request.POST.get('statut')
        date_echeance = request.POST.get('date_echeance') or None
        temps_estime = request.POST.get('temps_estime') or None
        temps_passe = request.POST.get('temps_passe') or None
        assignee_id = request.POST.get('assignee')
        
        if not titre:
            messages.error(request, "Le titre de la tâche est obligatoire.")
            return redirect('edit_task', tache_id=tache.id)
        
        # Mettre à jour la tâche
        tache.titre = titre
        tache.description = description
        tache.priorite = priorite
        tache.statut = statut
        tache.date_echeance = date_echeance
        tache.temps_estime = temps_estime
        tache.temps_passe = temps_passe
        
        # Assigner la tâche si un utilisateur est sélectionné
        if assignee_id:
            assignee = get_object_or_404(User, id=assignee_id)
            tache.assignee = assignee
        else:
            tache.assignee = None
        
        tache.save()
        messages.success(request, f"La tâche '{tache.titre}' a été mise à jour avec succès.")
        return redirect('task_detail', tache_id=tache.id)
    
    # Pour le formulaire GET
    # Récupérer les membres du projet pour l'assignation
    membres_projet = list(projet.membres.all())
    if projet.chef_de_projet not in membres_projet:
        membres_projet.append(projet.chef_de_projet)
    
    context = {
        'tache': tache,
        'projet': projet,
        'membres_projet': membres_projet,
    }
    
    return render(request, 'edit_task.html', context)

@login_required
def update_task_status(request, tache_id):
    """Mettre à jour rapidement le statut d'une tâche"""
    if request.method == 'POST':
        tache = get_object_or_404(Tache, id=tache_id)
        projet = tache.projet
        
        # Vérifier que l'utilisateur a le droit de modifier cette tâche
        if request.user != projet.chef_de_projet and request.user != tache.assignee and request.user not in projet.membres.all():
            messages.error(request, "Vous n'avez pas l'autorisation de modifier cette tâche.")
            return redirect('task_detail', tache_id=tache.id)
        
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in [s[0] for s in Tache.STATUT_CHOICES]:
            tache.statut = nouveau_statut
            tache.save()
            messages.success(request, f"Le statut de la tâche a été mis à jour en '{tache.get_statut_display()}'.")
        
        # Rediriger vers la page précédente ou la page de détail
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('task_detail', tache_id=tache.id)
    
    return redirect('task_list')

@login_required
def add_comment(request, tache_id):
    """Ajouter un commentaire à une tâche"""
    tache = get_object_or_404(Tache, id=tache_id)
    projet = tache.projet
    
    # Vérifier que l'utilisateur a accès à cette tâche
    if request.user != projet.chef_de_projet and request.user not in projet.membres.all() and request.user != tache.assignee:
        messages.error(request, "Vous n'avez pas accès à cette tâche.")
        return redirect('task_list')
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Commentaire.objects.create(
                tache=tache,
                auteur=request.user,
                contenu=contenu
            )
            messages.success(request, "Votre commentaire a été ajouté.")
        
    return redirect('task_detail', tache_id=tache.id)
