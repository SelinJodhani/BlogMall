from users.models import Profile
from django.contrib.auth import models, authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, request, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from django.contrib.auth.models import User, UserManager
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView

# Create your views here.

# def home(request):
#     context = {
#         'posts': Post.objects.all(),
#         'title': 'Home'
#     }
#     return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class TagView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

class SearchView(ListView):
    model = Post
    template_name = 'blog/search_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET['query'])

    def get_context_data(self, **kwargs):
        path = self.request.get_full_path
        query = self.request.GET['query']          
        context = super().get_context_data(**kwargs)                     
        context['query'] = query
        context['path'] = path
        print(path)
        return context

class PostDetailView(HitCountDetailView, DetailView):
    model = Post
    count_hit = True

    def get_context_data(self, *arge, **kwargs):

        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False

        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        context['id'] = self.kwargs['pk']

        return context

    # Comment Section
    def post(self,request, *args ,pk,**kwargs):

        if request.method == 'POST': 

            if request.user:
                body = request.POST.get('body')
                post_id = request.POST.get('post_id')
                url = request.POST.get('url')

                data = Comment(
                    post = Post.objects.get(id = int(post_id)),
                    user = request.user,
                    body = body,
                )
                data.save()
                
        return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def TagListView(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'posts':posts,
    }
    return render(request, 'blog/base.html', context)

def about(request):
    context = {
        'title' : 'About'
    }
    return render(request, 'blog/about.html', context)