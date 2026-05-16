from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    A simple model representing a blog post.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    image = models.ImageField(default='default_post.jpg', upload_to='post_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def plain_text(self):
        """
        Returns the content stripped of markdown formatting for summaries.
        """
        import re
        text = self.content
        # Strip code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Strip inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Strip images: ![alt](url) -> ""
        text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', text)
        # Strip links: [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Strip bold/italic: **text** or *text* -> text
        text = re.sub(r'[*_]{1,3}([^*_]+)[*_]{1,3}', r'\1', text)
        # Strip headers: # Header -> Header
        text = re.sub(r'#+\s*(.*)', r'\1', text)
        # Strip horizontal rules
        text = re.sub(r'^-{3,}|^\*{3,}|^\_{3,}', '', text, flags=re.MULTILINE)
        # Strip blockquotes
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        # Strip list markers
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        
        return text.strip()

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        name = self.user.username if self.user else self.author_name
        return f'Comment by {name} on {self.post.title}'
