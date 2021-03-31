from blog.models import Post

def tags_processor(request):
    common_tags = Post.tags.most_common()
    return {'common_tags': common_tags}