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

    def __str__(self):
        return self.name


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
        verbose_name = "series"
        verbose_name_plural = "series"

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class ItemType(models.Model):
    """
    Represents type of the item. It can be either player stream, video or just url.
    """
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "libertv_item_types"
        ordering = ["name"]
        verbose_name = "item type"
        verbose_name_plural = "item types"

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Represents an items, which can be in its basic extendable form either a url for the browser
    or a url for the media player
    """
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=510)
    description = models.TextField(null=True)
    address = models.CharField(max_length=2048, null=True)
    data = models.JSONField(null=True)
    position = models.IntegerField()
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    series = models.ManyToManyField(Series, null=True)
    categories = models.ManyToManyField(Category, null=True)
    tags = models.ManyToManyField(Tag, null=True)

    class Meta:
        db_table = "libertv_items"
        ordering = ["position"]
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        return self.name
