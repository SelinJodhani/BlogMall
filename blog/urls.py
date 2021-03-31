from django.urls import path, include
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, LikeView, TagView, SearchView
from blog import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('tags/<slug:tag_slug>/', TagView.as_view(), name='tag-posts'),
    path('search/', SearchView.as_view(), name='search-posts'),
    path('about/', views.about, name='blog-about'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]