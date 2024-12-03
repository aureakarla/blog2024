from django.shortcuts import render,redirect, get_object_or_404
from .forms import NoticiaForm, NoticiaFilterForm
from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria
from .forms import CategoriaForm
from django.core.paginator import Paginator

# Create your views here.
@login_required
def inicio_gerencia(request):
    return render(request, 'gerencia/inicio.html')

def listagem_noticia(request):
    formularioFiltro = NoticiaFilterForm(request.GET or None)
    
    noticias = Noticia.objects.filter(usuario=request.user)  

    if formularioFiltro.is_valid():
        if formularioFiltro.cleaned_data['titulo']:
            noticias = noticias.filter(titulo__icontains=formularioFiltro.cleaned_data['titulo'])
        if formularioFiltro.cleaned_data['data_publicacao_inicio']:
            noticias = noticias.filter(data_publicacao__gte=formularioFiltro.cleaned_data['data_publicacao_inicio'])
        if formularioFiltro.cleaned_data['data_publicacao_fim']:
            noticias = noticias.filter(data_publicacao__lte=formularioFiltro.cleaned_data['data_publicacao_fim'])
        if formularioFiltro.cleaned_data['categoria']:
            noticias = noticias.filter(categoria=formularioFiltro.cleaned_data['categoria'])
    
    contexto = {
        'noticias': noticias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_noticia.html',contexto)


def cadastrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  
            noticia.usuario = request.user  
            noticia.save()  
            return redirect('gerencia:listagem_noticia')  
    else:
        form = NoticiaForm() 

    contexto = {'form': form}
    return render(request, 'gerencia/cadastro_noticia.html', contexto)

@login_required
def editar_noticia(request, id):
    noticia = Noticia.objects.get(id=id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia_editada = form.save(commit=False) 
            noticia_editada.usuario = request.user
            noticia_editada.save()  
            return redirect('gerencia:listagem_noticia')
    else:
        form = NoticiaForm(instance=noticia)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_noticia.html',contexto)




def index(request):
    categoria_nome = request.GET.get('categoria')  
    search_query = request.GET.get('search')  

   
    noticias = Noticia.objects.all()
    if categoria_nome:
        categoria = Categoria.objects.filter(nome=categoria_nome).first()
        if categoria:
            noticias = noticias.filter(categoria=categoria)

    if search_query:
        noticias = noticias.filter(titulo__icontains=search_query)  

    categorias = Categoria.objects.all() 

    contexto = {
        'noticias': noticias,
        'categorias': categorias,
        'categoria_selecionada': categoria_nome,
        'search_query': search_query,
    }
    return render(request, 'gerencia/index.html', contexto)


@login_required
def listar_categ(request):
    search_query = request.GET.get('search', '')

    if search_query:
        categorias = Categoria.objects.filter(nome__icontains=search_query).order_by('nome')
    else:
        categorias = Categoria.objects.all().order_by('nome')

    paginator = Paginator(categorias, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'gerencia/listar_categ.html', contexto)

    
@login_required
def criar_categ(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerencia:listar_categ')
    else:
        form = CategoriaForm()
    return render(request, 'gerencia/criar_categ.html', {'form': form})

@login_required
def editar_categ(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('gerencia:listar_categ')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'gerencia/editar_categ.html', {'form': form})

@login_required
def deletar_categ(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('gerencia:listar_categ')
    return render(request, 'gerencia/deletar_categ.html', {'categoria': categoria})