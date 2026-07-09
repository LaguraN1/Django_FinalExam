from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "tags",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Post title",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Write your post...",
                }
            ),
            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_published": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            raise forms.ValidationError(
                "Title must be at least 5 characters long."
            )

        return title


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            "body",
        ]

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write a comment...",
                }
            ),
        }

    def clean_body(self):
        body = self.cleaned_data.get("body")

        if len(body) < 2:
            raise forms.ValidationError(
                "Comment is too short."
            )

        return body