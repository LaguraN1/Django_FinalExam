from django import forms

from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    tag_names = forms.CharField(
        required=False,
        label="Tags",
        help_text="Write tags separated by commas. Example: django, python, web",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "django, python, web",
            }
        )
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "tag_names",
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
            "is_published": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            tags = self.instance.tags.all()
            self.fields["tag_names"].initial = ", ".join(
                tag.name for tag in tags
            )

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            raise forms.ValidationError(
                "Title must be at least 5 characters long."
            )

        return title

    def clean_tag_names(self):
        tag_names = self.cleaned_data.get("tag_names", "")

        tags = [
            tag.strip()
            for tag in tag_names.split(",")
            if tag.strip()
        ]

        if len(tags) > 5:
            raise forms.ValidationError(
                "You can add maximum 5 tags."
            )

        return tags

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

            tags = []

            for tag_name in self.cleaned_data["tag_names"]:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name
                )

                tags.append(tag)

            post.tags.set(tags)

        return post


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