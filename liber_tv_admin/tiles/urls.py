from django.urls import path

from .views import (
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView,
    CategoryDeleteView, ItemsView, SeriesView
)

urlpatterns = [
    path("category/", CategoryListView.as_view(), name="categories_list"),
    path('category/<int:pk>/detail', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path("items/", ItemsView.as_view(), name="items_all"),
    path("items/<int:category_id>", ItemsView.as_view(), name="items"),
    path("series/", SeriesView.as_view(), name="series_all"),
    path("series/<int:category_id>", SeriesView.as_view(), name="series"),
    # path('item/<int:pk>/detail', ItemDetailView.as_view(), name='item_detail'),
    # path('item/create/', ItemCreateView.as_view(), name='item_create'),
    # path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    # path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
]
