from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class SearchContextMixin:
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context