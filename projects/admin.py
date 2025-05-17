from django.contrib import admin

# Register your models here.


from .models import Projet, CategorieProjet

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'chef_de_projet', 'date_creation', 'statut', 'priorite')
    list_filter = ('statut', 'priorite', 'chef_de_projet')
    search_fields = ('nom', 'description')
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'
    list_per_page = 10
    list_editable = ('statut', 'priorite')



@admin.register(CategorieProjet)
class CategorieProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'projet')
    list_filter = ('projet',)
    search_fields = ('nom', 'description')
    ordering = ('nom',)
    list_per_page = 10


    