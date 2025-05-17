
from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.project_list, name='project_list'),
    path('<int:projet_id>/', views.project_detail, name='project_detail'),
    path('<int:projet_id>/edit/', views.edit_project, name='edit_project'),
    path('add/', views.add_project, name='add_project'),
    path('<int:projet_id>/add-task/', views.add_task, name='add_task'),
]
