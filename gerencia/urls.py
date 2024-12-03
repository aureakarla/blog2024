from django.urls import path
from .views import inicio_gerencia, listagem_noticia,cadastrar_noticia,editar_noticia, listar_categ, criar_categ, editar_categ, deletar_categ

app_name = 'gerencia'

urlpatterns = [
    path('', inicio_gerencia, name='gerencia_inicial'),
    path('noticias/', listagem_noticia, name='listagem_noticia'),
    path('noticias/cadastro', cadastrar_noticia, name='cadastro_noticia'),
    path('noticias/editar/<int:id>', editar_noticia, name='editar_noticia'),
    path('categorias/', listar_categ, name='listar_categ'),
    path('categorias/criar/', criar_categ, name='criar_categ'),
    path('categorias/editar/<int:id>/', editar_categ, name='editar_categ'),
    path('categorias/deletar/<int:id>/', deletar_categ, name='deletar_categ'),
]