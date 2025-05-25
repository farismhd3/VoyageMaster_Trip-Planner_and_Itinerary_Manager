from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Discussion, Post, Comment
from destination.models import Destination
from .forms import DiscussionForm, PostForm, CommentForm
from django.urls import reverse




def discussion_list(request):
    discussions = Discussion.objects.filter(is_active=True).order_by('-created_at')
    destinations = Destination.objects.all()
    return render(request, 'community/discussion_list.html', {
        'discussions': discussions,
        'destinations': destinations
    })

@login_required
def create_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.creator = request.user
            discussion.save()
            messages.success(request, 'Discussion created successfully!')
            return redirect(reverse('community:discussion_detail', kwargs={'pk': discussion.pk}))

    else:
        form = DiscussionForm()

    # Check if user is from agency app
    is_agency = hasattr(request.user, 'agency')
    template_name = 'community/agency_create_discussion.html' if is_agency else 'community/create_discussion.html'
    
    return render(request, template_name, {'form': form})

def delete_discussion(request, discussion_pk):
    discussion = get_object_or_404(Discussion, pk=discussion_pk)
    if discussion.creator == request.user:  # Ensure the user is the creator of the discussion
        discussion.is_active = False  # Soft delete by marking as inactive
        discussion.save()
        return redirect('/travel_agency_dashboard')
    else:
        messages.error(request, 'You do not have permission to delete this discussion.')
        return redirect('community:discussion_detail', pk=pk)
   
   
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    posts = discussion.posts.all().order_by('-created_at')
    return render(request, 'community/discussion_detail.html', {
        'discussion': discussion,
        'posts': posts
    })

@login_required
def create_post(request, discussion_pk):
    discussion = get_object_or_404(Discussion, pk=discussion_pk)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.discussion = discussion
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')

            return redirect(reverse('community:discussion_detail', kwargs={'pk': discussion_pk}))

    else:
        form = PostForm()
    return render(request, 'community/create_post.html', {
        'form': form,
        'discussion': discussion
    })

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:  # Ensure the user is the author of the post
        post.delete()
    return redirect('community:discussion_detail', pk=post.discussion.pk) 

@login_required
def like_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })

@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('community:discussion_detail', pk=post.discussion.pk)
    else:
        form = CommentForm()
    return render(request, 'community/create_comment.html', {
        'form': form,
        'post': post
    })



@login_required
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes()
        })

    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)