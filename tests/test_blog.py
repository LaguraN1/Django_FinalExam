import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from blog.models import Post, Comment, Like, Bookmark, Follow
from blog.services.interaction_service import InteractionService
from blog.services.post_service import PostService


User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="user1",
        password="testpass123"
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="user2",
        password="testpass123"
    )


@pytest.fixture
def post(db, user):
    return Post.objects.create(
        user=user,
        title="Test Post Title",
        body="This is a test post body.",
        is_published=True
    )


@pytest.mark.django_db
def test_post_is_created_with_slug(post):
    assert post.slug != ""


@pytest.mark.django_db
def test_home_page_loads(client, post):
    url = reverse("blog:post-list")
    response = client.get(url)

    assert response.status_code == 200
    assert b"Test Post Title" in response.content


@pytest.mark.django_db
def test_post_detail_page_loads(client, post):
    url = reverse(
        "blog:post-detail",
        kwargs={"slug": post.slug}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert b"Test Post Title" in response.content


@pytest.mark.django_db
def test_create_post_requires_login(client):
    url = reverse("blog:post-create")
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_logged_in_user_can_comment(client, user, post):
    client.login(
        username="user1",
        password="testpass123"
    )

    url = reverse(
        "blog:comment-create",
        kwargs={"slug": post.slug}
    )

    response = client.post(
        url,
        {
            "body": "Nice comment"
        }
    )

    assert response.status_code == 302
    assert Comment.objects.filter(post=post).count() == 1


@pytest.mark.django_db
def test_like_is_idempotent(user, post):
    InteractionService.like_post_idempotent(user, post)
    InteractionService.like_post_idempotent(user, post)
    InteractionService.like_post_idempotent(user, post)

    count = Like.objects.filter(
        user=user,
        post=post
    ).count()

    assert count == 1


@pytest.mark.django_db
def test_bookmark_is_idempotent(user, post):
    InteractionService.bookmark_post_idempotent(user, post)
    InteractionService.bookmark_post_idempotent(user, post)
    InteractionService.bookmark_post_idempotent(user, post)

    count = Bookmark.objects.filter(
        user=user,
        post=post
    ).count()

    assert count == 1


@pytest.mark.django_db
def test_follow_is_idempotent(user, other_user):
    InteractionService.follow_user(user, other_user)
    InteractionService.follow_user(user, other_user)
    InteractionService.follow_user(user, other_user)

    count = Follow.objects.filter(
        follower=user,
        following=other_user
    ).count()

    assert count == 1


@pytest.mark.django_db
def test_trending_score_returns_number(post):
    score = PostService.calculate_trending_score(post)

    assert isinstance(score, float)


@pytest.mark.django_db
def test_api_posts_list_loads(client, post):
    url = reverse("api:post-list-create")
    response = client.get(url)

    assert response.status_code == 200