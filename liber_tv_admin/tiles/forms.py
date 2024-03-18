from django import forms

from .models import Category, Item, Series, ItemType


class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=True)
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ("name", "position", "parent")

    def __init__(self, *args, **kwargs):

        # TODO: add parent category from url eg. category/{id}
        kwargs.update(initial={
            'position': Category.objects.filter(parent__isnull=True).count()
        })

        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SeriesForm(forms.ModelForm):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    category = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    tags_list = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)

    class Meta:
        model = Series
        fields = ("name", "description", "address", "tags_list", "position", "parent")

    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'position': Series.objects.count()
        })

        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ItemForm(forms.ModelForm):
    name = forms.CharField(required=True)
    title = forms.CharField(required=True)
    address = forms.CharField(required=True)
    serie = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    category = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    tags_list = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)
    data = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)
    type = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=ItemType.objects.all())

    class Meta:
        model = Item
        fields = ("name", "title", "description", "address", "data", "position", "type", "category", "serie")

    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'position': Item.objects.filter(series__isnull=True).count()
        })

        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields["type"].widget.attrs['class'] = 'form-inline'
