from django.db import models, InternalError


def SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT_BRAND(collector, field, sub_objs, using):
    """
    ``sub_objs`` is the Queryset of Items that are affected by this delete.
    Hence, none of them should have referenced the default User (Otherwise,
    the default User is going to be deleted!).
    Also, if we are deleting an Item, there should be a default User to
    be set as the new User of Item.
    """
    try:
        default_brand = Brand.objects.get(name="default")
    except Brand.DoesNotExist:
        raise InternalError("You should have default brand before deleting a referenced brand")
    
    for item in sub_objs:
        if item.brand == default_brand:
            raise InternalError("You cannot delete default brand when there are items referencing it")

    collector.add_field_update(field, default_brand, sub_objs)


def SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT_CATEGORY(collector, field, sub_objs, using):
    """
    ``sub_objs`` is the Queryset of Items that are affected by this delete.
    Hence, none of them should have referenced the default User (Otherwise,
    the default User is going to be deleted!).
    Also, if we are deleting an Item, there should be a default User to
    be set as the new User of Item.
    """
    
    try:
        default_category = Category.objects.get(name="default")
    except Category.DoesNotExist:
        raise InternalError("You should have default category before deleting a referenced category")
    
    for item in sub_objs:
        if item.category == default_category:
            raise InternalError("You cannot delete default category when there are items referencing it")

    collector.add_field_update(field, default_category, sub_objs)


class Brand(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, db_index=True, blank=False)
    slug = models.SlugField(max_length=250, unique=True, blank=False)
    show = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "brands"

    def __str__(self):
        return f"{self.name}"
    

class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, db_index=True, blank=False)
    slug = models.SlugField(max_length=250, unique=True, blank=False)
    show = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, blank=False)
    brand = models.ForeignKey(Brand, default=1, on_delete=SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT_BRAND)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, default=1, on_delete=SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT_CATEGORY)
    show = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return f"{self.title} ({self.category}/{self.brand})"
