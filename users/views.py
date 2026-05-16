from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    """
    View for user registration.
    If the request is POST, it processes the form data.
    If GET, it displays an empty registration form.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """
    View for user profile. Allows user to update their info.
    """
    from .models import Profile
    from blog.models import Post, Bookmark
    from django.db.models import Sum
    from django.http import JsonResponse
    
    Profile.objects.get_or_create(user=request.user)
    
    posts = Post.objects.filter(author=request.user)
    post_count = posts.count()
    total_views = posts.aggregate(Sum('views'))['views__sum'] or 0
    
    # Calculate total likes across all user's posts
    total_likes = 0
    for post in posts:
        total_likes += post.likes.count()

    # Handle Polling
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'post_count': post_count,
            'total_views': total_views,
            'total_likes': total_likes
        })

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    # Get Bookmarked posts
    bookmarked_posts = [b.post for b in Bookmark.objects.filter(user=request.user).select_related('post', 'post__author')]

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'bookmarked_posts': bookmarked_posts,
        'post_count': post_count,
        'total_views': total_views,
        'total_likes': total_likes
    }
    
    return render(request, 'users/profile.html', context)
