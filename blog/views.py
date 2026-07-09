from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .services.post_service import PostService
from .services.interaction_service import InteractionService
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Comment, Like, Bookmark, Follow
from .forms import PostForm, CommentForm
from django.db.models import Q

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")

        queryset = Post.objects.published().select_related(
        "user"
        ).prefetch_related(
        "tags"
        ).order_by("-created_at")

        if query:
            queryset = queryset.search(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post-list")

def form_valid(self, form):
    form.instance.user = self.request.user

    messages.success(
        self.request,
        "Post created successfully."
    )

    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "blog:post-detail",
            kwargs={"slug": self.object.slug}
        )

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user
    
    def form_valid(self, form):
        messages.success(
            self.request,
            "Post updated successfully."
        )
        return super().form_valid(form)



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            slug=self.kwargs["slug"]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post-detail",
            kwargs={"slug": self.kwargs["slug"]}
        )


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "blog:post-detail",
            kwargs={"slug": self.object.post.slug}
        )


class ProfileView(DetailView):
    model = User
    template_name = "blog/profile.html"
    context_object_name = "profile_user"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["followers_count"] = self.object.followers.count()
        context["following_count"] = self.object.following.count()
        context["user_posts"] = self.object.posts.all().order_by("-created_at")

        if self.request.user.is_authenticated:
            context["is_following"] = Follow.objects.filter(
                follower=self.request.user,
                following=self.object
            ).exists()
        else:
            context["is_following"] = False

        return context


# --- Function Based Views ---


@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if request.method == "POST":
        body = request.POST.get("body")

        if body and body.strip():
            Comment.objects.create(
                user=request.user,
                post=parent_comment.post,
                parent=parent_comment,
                body=body
            )

    return redirect(
        "blog:post-detail",
        slug=parent_comment.post.slug
    )


@login_required
def like_post(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug
    )

    liked = InteractionService.toggle_like(
        request.user,
        post
    )

    if liked:
        messages.success(
            request,
            "Post liked."
        )
    else:
        messages.info(
            request,
            "Post unliked."
        )

    return redirect(
        "blog:post-detail",
        slug=slug
    )
    post = get_object_or_404(
        Post,
        slug=slug
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect(
        "blog:post-detail",
        slug=slug
    )


@login_required
def bookmark_post(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug
    )

    saved = InteractionService.toggle_bookmark(
        request.user,
        post
    )

    if saved:
        messages.success(
            request,
            "Post saved."
        )
    else:
        messages.info(
            request,
            "Bookmark removed."
        )

    return redirect(
        "blog:post-detail",
        slug=slug
    )
    post = get_object_or_404(
        Post,
        slug=slug
    )

    bookmark = Bookmark.objects.filter(
        user=request.user,
        post=post
    )

    if bookmark.exists():
        bookmark.delete()
    else:
        Bookmark.objects.create(
            user=request.user,
            post=post
        )

    return redirect(
        "blog:post-detail",
        slug=slug
    )


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    followed = InteractionService.follow_user(
        request.user,
        user_to_follow
    )

    if followed:
        messages.success(
            request,
            f"You followed {user_to_follow.username}."
        )

    return redirect(
        "blog:profile",
        username=username
    )
    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect(
        "blog:profile",
        username=username
    )


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(
        User,
        username=username
    )

    unfollowed = InteractionService.unfollow_user(
        request.user,
        user_to_unfollow
    )

    if unfollowed:
        messages.info(
            request,
            f"You unfollowed {user_to_unfollow.username}."
        )

    return redirect(
        "blog:profile",
        username=username
    )
    user_to_unfollow = get_object_or_404(
        User,
        username=username
    )

    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()

    return redirect(
        "blog:profile",
        username=username
    )


class MyBookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = "blog/bookmarks.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        return Bookmark.objects.filter(
            user=self.request.user
        ).select_related("post").order_by("-created_at")
    


