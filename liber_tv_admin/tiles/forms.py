from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Category
        fields = ("name", "position", "parent")

    def __init__(self, *args, **kwargs):
        print(args)
        print(kwargs)
        kwargs.update(initial={
            'position': Category.objects.count()
        })

        super().__init__(*args, **kwargs)
