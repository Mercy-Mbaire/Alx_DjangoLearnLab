from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm
from .models import Post, Comment


def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """Handle user profile view and updates"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})


# Blog Post CRUD Views

class PostListView(ListView):
    """Display all blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailView(DetailView):
    """Display a single blog post and its comments"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post (authenticated users only)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        """Set the author to the current logged-in user"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a blog post (author only)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the author to the current logged-in user"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        """Redirect to the post detail page after update"""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post (author only)"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    context_object_name = 'post'
    
    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """Add success message when post is deleted"""
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Comment CRUD Views

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create a new comment on a post"""
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a comment (author only)"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment (author only)"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


