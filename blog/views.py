from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Post, Category, Comment, Bookmark
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            from django.db.models import Case, When, Value, IntegerField
            queryset = queryset.filter(
                Q(author__username__icontains=query) |
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).annotate(
                relevance=Case(
                    When(author__username__icontains=query, then=Value(3)),
                    When(title__icontains=query, then=Value(2)),
                    When(content__icontains=query, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by('-relevance', '-date_posted')
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get(self, request, *args, **kwargs):
        # Handle AJAX search/filter requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            html = render_to_string('blog/_post_list.html', {
                'posts': self.object_list,
                'page_obj': None # Pagination might need careful handling for AJAX
            }, request=request)
            return JsonResponse({'html': html})
            
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Increment views
        self.object.views += 1
        self.object.save()
        context['comments'] = self.object.comments.filter(parent__isnull=True).order_by('-created_at')
        if self.request.user.is_authenticated:
            context['is_liked'] = self.object.likes.filter(id=self.request.user.id).exists()
            context['is_bookmarked'] = Bookmark.objects.filter(user=self.request.user, post=self.object).exists()
        else:
            context['is_liked'] = False
            context['is_bookmarked'] = False
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Polling check: if last_id is provided, return only newer comments
        last_id = request.GET.get('last_id')
        if last_id and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            new_comments = self.object.comments.filter(id__gt=last_id, parent__isnull=True).order_by('created_at')
            html = ""
            for comment in new_comments:
                html += render_to_string('blog/_comment.html', {
                    'comment': comment,
                    'user': self.request.user,
                    'is_last': False
                }, request=self.request)
            
            return JsonResponse({
                'html': html,
                'new_count': new_comments.count(),
                'latest_id': new_comments.last().id if new_comments.exists() else last_id,
                'total_comments': self.object.comments.count(),
                'total_likes': self.object.likes.count()
            })
            
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Handle Like Action
        if request.POST.get('action') == 'like' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'error': 'auth_required'})
            
            is_liked = False
            if self.object.likes.filter(id=request.user.id).exists():
                self.object.likes.remove(request.user)
            else:
                self.object.likes.add(request.user)
                is_liked = True
            
            return JsonResponse({
                'success': True,
                'total_likes': self.object.likes.count(),
                'is_liked': is_liked
            })

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        if self.request.user.is_authenticated:
            comment.user = self.request.user
        
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            comment.parent = parent_comment
            
        comment.save()

        # Check if it's an AJAX request
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('blog/_comment.html', {
                'comment': comment,
                'user': self.request.user,
                'is_last': True  # For AJAX, it's usually at the end or we don't want a border yet
            }, request=self.request)
            
            return JsonResponse({
                'success': True,
                'html': html,
                'parent_id': parent_id or None,
                'comment_id': comment.id
            })

        return super().form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Security check: ensure it's an image
        if not image.content_type.startswith('image/'):
            return JsonResponse({'error': 'File is not an image'}, status=400)
            
        # Generate a unique filename to prevent collisions
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return JsonResponse({'error': 'Unsupported image format'}, status=400)
            
        filename = f"{uuid.uuid4()}{ext}"
        
        # Save the file
        path = default_storage.save(os.path.join('post_images', filename), ContentFile(image.read()))
        url = os.path.join(settings.MEDIA_URL, path).replace('\\', '/')
        
        return JsonResponse({
            'data': {
                'filePath': url
            }
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

class BookmarkToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
            
            if not created:
                bookmark.delete()
                is_bookmarked = False
            else:
                is_bookmarked = True
                
            return JsonResponse({'is_bookmarked': is_bookmarked})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
