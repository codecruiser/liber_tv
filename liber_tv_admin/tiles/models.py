from django.db import models


class Category(models.Model):
    """
    Represents top category tile from which one chooses a subject
    """
    name = models.CharField(max_length=255)
    position = models.IntegerField()
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "libertv_categories"
        ordering = ["position"]
        verbose_name = "category"
        verbose_name_plural = "categories"


class Series(models.Model):
    """
    Represents series which connects some items based on: time, a common subject, as a playlist etc.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    position = models.IntegerField()
    parent = models.ForeignKey("Series", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "libertv_series"
        ordering = ["position"]
        verbose_name = "serie"
        verbose_name_plural = "series"


class Tag(models.Model):
    """
    Represents items' tag used to narrow the items to an interesting set
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "libertv_tags"
        ordering = ["name"]
        verbose_name = "tag"
        verbose_name_plural = "tags"


class TagCategory(models.Model):
    """
    Groups tag into categories to allow better management.
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "libertv_tag_categories"
        ordering = ["name"]
        verbose_name = "tag category"
        verbose_name_plural = "tag categories"


class Item(models.Model):
    """
    Represents an items, which can be in its basic extendable form either a url for the browser
    or a url for the media player
    """
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=510)
    description = models.TextField(null=True)
    action = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=2048, null=True)
    position = models.IntegerField()
    series = models.ManyToManyField(Series, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "libertv_items"
        ordering = ["position"]
        verbose_name = "item"
        verbose_name_plural = "items"
