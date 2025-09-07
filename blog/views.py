def posts_by_category(request, category_id):
	category = get_object_or_404(Category, pk=category_id)
	posts = BlogPost.objects.filter(category=category).order_by('-created_at')
	categories = Category.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories, 'selected_category': category})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import BlogPost, Category
from .forms import BlogPostForm

def post_list(request):
	posts = BlogPost.objects.all().order_by('-created_at')
	categories = Category.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories})

def post_detail(request, slug):
	post = get_object_or_404(BlogPost, slug=slug)
	categories = Category.objects.all()
	return render(request, 'blog/post_detail.html', {'post': post, 'categories': categories})

@login_required
def post_create(request):
	if request.method == 'POST':
		form = BlogPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = BlogPostForm()
	categories = Category.objects.all()
	return render(request, 'blog/post_form.html', {'form': form, 'categories': categories})

@login_required
def post_edit(request, slug):
	post = get_object_or_404(BlogPost, slug=slug)
	if post.author != request.user:
		return redirect('post_detail', slug=post.slug)
	if request.method == 'POST':
		form = BlogPostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			return redirect('post_detail', slug=post.slug)
	else:
		form = BlogPostForm(instance=post)
	categories = Category.objects.all()
	return render(request, 'blog/post_form.html', {'form': form, 'categories': categories})

@login_required
def post_delete(request, slug):
	post = get_object_or_404(BlogPost, slug=slug)
	if post.author != request.user:
		return redirect('post_detail', slug=post.slug)
	if request.method == 'POST':
		post.delete()
		return redirect('post_list')
	categories = Category.objects.all()
	return render(request, 'blog/post_confirm_delete.html', {'post': post, 'categories': categories})

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('post_list')
	else:
		form = UserCreationForm()
	return render(request, 'registration/register.html', {'form': form})

def user_login(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('post_list')
	else:
		form = AuthenticationForm()
	return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
	logout(request)
	return redirect('post_list')

# Create your views here.
