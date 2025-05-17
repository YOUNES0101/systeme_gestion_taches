from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.task_list, name='task_list'),
    path('<int:tache_id>/', views.task_detail, name='task_detail'),
    path('<int:tache_id>/edit/', views.edit_task, name='edit_task'),
    path('<int:tache_id>/status/', views.update_task_status, name='update_task_status'),
    path('<int:tache_id>/comment/', views.add_comment, name='add_comment'),
]
