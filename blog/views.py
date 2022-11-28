
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm, UserRegistrationForm, UserEditForm   
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')	
    return render(request, 'blog/post_list.html', {'posts': posts})
    

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.imagen = request.FILES.get( 'image')
            post.short_text = request.POST.get('short_text')
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.imagen = request.FILES.get( 'image')
            post.short_text = request.POST.get('short_text')
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



def login_request(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      usuario = form.cleaned_data.get('username')
      clave = form.cleaned_data.get('password')
      user = authenticate(username=usuario, password=clave) 
      if user is not None:
        login(request,user) 
        return redirect('post_list')
      else:
        return render(request, 'blog/post_list.html', {'mensaje': 'Error, datos incorrectos'})
    else:
        return render(request, 'blog/post_list.html', {'mensaje': 'Usuario o clave incorrectos' })
  else:
    form = AuthenticationForm() 
    return render(request, 'blog/login.html', {'form':form})

def register (request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            global username
            username=form.cleaned_data['username']   
            form.save()
        return render (request, 'blog/post_list.html', {'mensaje': 'Usuario creado correctamente'})
      
    else:
        form = UserRegistrationForm()
        return render(request, 'blog/register.html', {'form':form})

@login_required
def editarPerfil(request):
  usuario = request.user

  if request.method == 'POST':
    formulario = UserEditForm(request.POST, instance=usuario)
    if formulario.is_valid():
      informacion = formulario.cleaned_data
      usuario.email = informacion['email']
      usuario.password1 = informacion['password1']
      usuario.password2 = informacion['password2']
      usuario.save()

      return render(request, 'blog/post_list.html', {'usuario': usuario, 'mensaje': 'Datos actualizados correctamente'})
  else:
    formulario = UserEditForm(instance=usuario)
  return render(request, 'blog/editarperfil.html', {'formulario': formulario, 'usuario': usuario.username})


def aboutme(request):
    return render(request, 'blog/aboutme.html')

def miperfil(request):
    return render(request, 'blog/miperfil.html')