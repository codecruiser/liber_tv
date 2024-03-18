from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import BaseCreateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CategoryForm, ItemForm, SeriesForm
from .models import Category, Series, Item
from .serializers import SeriesSerializer


class CategoryBaseView(View):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('categories_list')


class CategoryListView(CategoryBaseView, ListView):
    template_name = "category.html"

    def construct_tree(self, categories, parent=None):
        tree = []
        for category in categories[parent]:
            data = {
                'id': category.id,
                'name': category.name
            }
            if category.id in categories:
                data["children"] = self.construct_tree(categories, category.id)
            data["children_count"] = len(data.get("children", []))
            tree.append(data)
        return tree

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = {}
        for cat in Category.objects.all():
            parent = cat.parent.id if cat.parent else None
            if parent not in categories:
                categories[parent] = []
            categories[parent].append(cat)
        cat_tree = self.construct_tree(categories)
        context["categories"] = cat_tree
        context["form"] = CategoryForm
        context["series_form"] = SeriesForm
        context["item_form"] = ItemForm
        return context


class CategoryDetailView(CategoryBaseView, DetailView):
    """"""


class CategoryCreateView(CategoryBaseView, CreateView):
    """"""


class CategoryUpdateView(CategoryBaseView, UpdateView):
    """"""


class CategoryDeleteView(CategoryBaseView, DeleteView):
    """"""


class ItemsView(APIView):

    def get(self, request, category_id, series_id=None):
        items = []
        for item in Item.objects.filter(categories__id__exact=category_id).all():
            items.append({
                'name': item.name,
                'title': item.title,
            })
        series = []
        return Response({"items": items, "series": series})

    def post(self, request):

        form = ItemForm(request.data)
        if form.is_valid():
                data = form.data.copy()
                category_id = request.data.get('category')
                series_id = request.data.get('serie')
                tags_list = request.data.get('tags_list')
                del data['csrfmiddlewaretoken']
                del data['category']
                obj = form.save()
                if category_id:
                    obj.categories.add(Category.objects.get(pk=int(category_id)))
                    obj.save()
                if series_id:
                    obj.series.add(Series.objects.get(pk=int(series_id)))
                    obj.save()
                return Response({"success": True, "series_id": True})
        else:
            print(form.errors)
            return Response({"success": False}, status=409)


class ItemView(BaseCreateView):
    model = Item
    fields = '__all__'
    success_url = reverse_lazy('categories_list')


class SeriesView(APIView):

    def get(self, request, category_id, series_id=None):
        series = []
        for item in Series.objects.filter(categories__id__exact=category_id).all():
            series.append({
                'id': item.id,
                'name': item.name,
            })
        return Response({"series": series})

    def post(self, request):

        form = SeriesForm(request.data)
        if form.is_valid():
            if form.data.get("series_id"):
                pass
            else:
                data = form.data.copy()
                category_id = request.data.get('category')
                tags_list = request.data.get('tags_list')
                del data['csrfmiddlewaretoken']
                del data['category']
                obj = form.save()
                obj.categories.add(Category.objects.get(pk=int(category_id)))
                obj.save()
                return Response({"success": True, "series_id": True})
        else:
            print(form.errors)
            return Response({"success": False}, status=409)
