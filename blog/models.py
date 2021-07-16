from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content  = RichTextField(blank=True, null=True)
    image = models.ImageField(default='', upload_to='post_pics')
    tags = TaggableManager()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})  

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.post} | {self.user}' 