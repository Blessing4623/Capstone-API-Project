from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import ProfileForm, PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
# Create your views here.
class RegisterView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login/')

@login_required()
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('profile/')
    else:
        form = ProfileForm()
    return render(request, 'blog/profile_edit.html', {'form': form})
@login_required()
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'blog/profile.html', {'profile': profile})
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post'
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
class PostUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/update.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    success_url = 'posts/'

class CommentListView(ListView):
    model = Comment
    # form_class = CommentForm
    context_object_name = 'comments'
    template_name = 'post_detail.html'
class CommentDetailView(DetailView):
    model = Comment
    # form_class = CommentForm
    context_object_name = 'comment'
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post_detail.html'
class CommentDeleteView(DeleteView):
    model = Comment
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'
def search_view(request):
    query = request.GET['q']
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)|
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        results = Post.objects.none()
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'search_results.html', context)
def tagged_posts_view(request, tag_name): 
    tag = get_object_or_404(Tag, name=tag_name) 
    posts = Post.objects.filter(tags=tag) 
    context = { 'tag': tag, 'posts': posts, }
    return render(request, 'tagged_posts.html', context)
class PostByTagListView(ListView):
    model = Tag
    form_class = PostForm