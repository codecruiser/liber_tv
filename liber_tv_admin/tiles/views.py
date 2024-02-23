from django.views.generic import FormView

from .forms import CategoryForm
from .models import Category


class CategoryView(FormView):
    template_name = "category.html"
    form_class = CategoryForm
    success_url = "/category/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = {}
        for cat in Category.objects.all():
            if cat not in categories:
                categories[cat.parent] = [cat]
            categories[cat.parent].append(categories)
        context["categories"] = Category.objects.all()
        return context
