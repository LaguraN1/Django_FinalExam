# Social Blog Platform

A Django 5 Social Blog Platform created as a final project.

## Project Description

This project is a social blog web application where users can register, log in, create posts, like posts, bookmark posts, comment, reply to comments, follow other users, and view trending posts.

The project uses Django, Django REST Framework, SQLite, Bootstrap, service layer classes, custom mixins, custom managers/querysets, automated tests, and an external avatar API.

---

## Student Information

Student ID: 5656  
Project: Project 20 — Social Blog Platform  
DRF Pattern: Generic API Views  
Reason: Student ID is even

---
## Live Demo

https://lagura.pythonanywhere.com/

## Admin URL

https://lagura.pythonanywhere.com/admin/

## Features

- User registration
- User login and logout
- Custom User model using `AbstractUser`
- User profiles
- DiceBear avatar external API
- Post create, read, update, delete
- Draft and published posts
- Tags
- Like and unlike posts
- Bookmark and remove bookmarks
- My Bookmarks page
- Follow and unfollow users
- Nested comments with 1-level replies
- Reading-time estimate
- Trending posts page
- Search posts by title, body, author, or tag
- Pagination with 10 posts per page
- Django messages framework
- Advanced Django Admin panel
- REST API with Django REST Framework
- Service layer classes
- Custom manager and queryset
- Custom class-based view mixins
- Automated tests with pytest-django
- Custom 404 and 500 error pages

---

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Bootstrap 5
- pytest
- pytest-django
- python-decouple
- DiceBear Avatar API
- Git and GitHub

---

## Django Apps

### `accounts`

Handles:

- Custom User model
- Register
- Login
- Logout
- User profile information
- Avatar URL support

### `blog`

Handles:

- Posts
- Tags
- Comments
- Likes
- Bookmarks
- Follows
- Trending posts
- Search
- Pagination
- Templates
- Services
- Mixins
- Managers

### `api`

Handles:

- REST API serializers
- REST API views
- API URLs

---

## Database Models

The main models used in the project are:

- `User`
- `Post`
- `Tag`
- `Comment`
- `Like`
- `Bookmark`
- `Follow`

Relationships include:

- One user can have many posts
- One post can have many comments
- One post can have many likes
- One post can have many bookmarks
- One user can follow many users
- One comment can have replies

---

## Authentication and Security

The project uses Django authentication:

- `django.contrib.auth`
- Custom User model
- `LoginRequiredMixin`
- `@login_required`
- CSRF protection in forms
- Password hashing
- Protected create, update, delete, like, bookmark, follow actions

---

## Forms

The project uses Django `ModelForm`.

Forms include custom validation with `clean_<field>()`.

Examples:

- Post title validation
- Comment body validation

CSRF tokens are used in POST forms.

---

## Class-Based Views and OOP

The project uses Django Class-Based Views:

- `ListView`
- `DetailView`
- `CreateView`
- `UpdateView`
- `DeleteView`

The project includes generic view overrides such as:

- `get_queryset`
- `get_context_data`
- `form_valid`
- `get_success_url`

---

Handles post-related business logic:

- Getting published posts
- Searching posts
- Getting user posts
- Calculating trending score
- Getting trending posts

### `InteractionService`

Handles user interaction logic:

- Like post
- Bookmark post
- Follow user
- Unfollow user
- Idempotent like
- Idempotent bookmark

---

## Custom Manager and QuerySet

The project includes a custom manager and queryset for posts.

Features:

- `published()`
- `drafts()`
- `search(query)`

This keeps query logic cleaner and reusable.

---

## Search and Pagination

Search is implemented using Django `Q` objects.

Users can search by:

- Post title
- Post body
- Author username
- Tag name

Pagination is enabled with:

```python
paginate_by = 10
```

---

## Reading Time Filter

The project includes a custom template filter:

```django
{{ post.body|read_time }}
```

It estimates how long it takes to read a post.

---

## Trending Algorithm

The project includes a signature algorithm for trending posts.

Formula:

```python
score = (likes - 1) / ((age_hours + 2) ** gravity)
```

Gravity used:

```python
gravity = 1.8
```

The algorithm gives higher scores to posts with more likes and lowers the score as posts get older.

---

## External API Integration

The project uses DiceBear Avatars as an external API.

Avatar URL format:

```text
https://api.dicebear.com/9.x/identicon/svg?seed=username
```

Each user gets a generated avatar based on their username.

---

## REST API

The project uses Django REST Framework.

Because the student ID is `5656`, which is even, the API is built using DRF generic views.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/posts/` | List all published posts |
| POST | `/api/posts/` | Create a new post |
| GET | `/api/posts/<slug>/` | Get post detail |
| POST | `/api/posts/<slug>/like/` | Like a post |
| GET | `/api/posts/<slug>/comments/` | List post comments |
| POST | `/api/posts/<slug>/comments/` | Create a comment |

---

## Concurrency and Idempotency

The project prevents duplicate likes, bookmarks, and follows.

It uses:

- `transaction.atomic()`
- `get_or_create()`
- `IntegrityError`
- Database `UniqueConstraint`

This means the same user cannot create duplicate likes, bookmarks, or follows.

Example:

```python
Like.objects.get_or_create(user=user, post=post)
```

---

## Admin Panel

The Django Admin panel is customized.

Registered models include:

- Posts
- Tags
- Comments
- Likes
- Bookmarks
- Follows

Admin features include:

- `list_display`
- `search_fields`
- `list_filter`
- Inline comments for posts

Admin URL:

```text
http://127.0.0.1:8000/admin/
```

---

## Automated Tests

The project includes automated tests using `pytest-django`.

Tests include:

- Post creation
- Slug generation
- Home page loading
- Post detail page loading
- Login requirement
- Comment creation
- Like idempotency
- Bookmark idempotency
- Follow idempotency
- Trending score
- API post list

Run tests:

```bash
pytest
```

Current result:

```text
10 passed
```

---

## Environment Variables

The project uses `python-decouple`.

Required environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

The `.env` file is not uploaded to GitHub.

The `.env.example` file is uploaded as an example.

---

## Project Structure

```text
Final_django_project/
├── accounts/
├── api/
├── blog/
│   ├── services/
│   ├── templatetags/
│   ├── managers.py
│   ├── mixins.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── config/
├── templates/
│   ├── 404.html
│   └── 500.html
├── tests/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── README.md
└── manage.py
```

---

## Error Handling

The project includes custom error pages:

- `404.html`
- `500.html`

These pages are used when `DEBUG=False`.

---

## GitHub

The project is uploaded to GitHub.

Repository:

```text
YOUR_REPOSITORY_URL
```

---

## Deployment

Planned deployment platform:

```text
PythonAnywhere
```

Deployment steps:

- Create PythonAnywhere web app
- Upload project to PythonAnywhere
- Create virtual environment
- Install requirements
- Add `.env`
- Run migrations
- Run collectstatic
- Configure WSGI
- Configure static files
- Set `DEBUG=False`
- Set `ALLOWED_HOSTS`

---
