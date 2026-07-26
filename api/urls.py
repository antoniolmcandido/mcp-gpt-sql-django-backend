from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("chat/", views.chat_endpoint, name="chat_endpoint"),
    path("alunos/", views.alunos_collection, name="alunos_collection"),
    path("alunos/<str:nome>/", views.aluno_detail, name="aluno_detail"),
]
