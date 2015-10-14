from django.db import models
from django.template.defaultfilters import slugify
from djangocms_text_ckeditor.fields import HTMLField


class ProductManager(models.Manager):
    """
    Product manager class.
    """
    def get_query_set(self):
        return super(ProductManager,
                     self).get_query_set().order_by('sort_id')


class ProductBase(models.Model):
    """
    Base product class. Contains all the fields necessary for
    a regular product. Just doesn't have versioning.
    """
    objects = ProductManager()
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = HTMLField(blank=True)
    image = models.ImageField("Image", max_length=200, upload_to="images", blank=True, null=True)
    documentation = models.FileField("PDF", max_length=200, upload_to="documents", blank=True, null=True)
    specifications = HTMLField(blank=True)
    category = models.ForeignKey('simplesjop.Category', related_name='products')
    slug = models.SlugField(max_length=255)
    sort_id = models.SmallIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Producten"

    def image_thumbnail(self):
        if self.image:
            return '<img src="%s" />' % self.image
        else:
            return ""
    image_thumbnail.allow_tags = True

    @models.permalink
    def get_absolute_url(self):
        # if self.category.parent:
        #     args = {
        #         'category_slug': self.category.parent.slug,
        #         'subcategory_slug': self.category.slug,
        #         'product_slug': self.slug
        #     }
        # else:
        #     args = {
        #         'category_slug': self.category.slug,
        #         'product_slug': self.slug
        #     }
        args = {
            'category_path': self.category.path,
            'product_id': self.pk,
            'product_slug': self.slug,
        }
        return ('product-view', (), args)


class Product(models.Model):
    """
    Product class to allow versions
    """
    base = models.ForeignKey('simplesjop.ProductBase', related_name="versions")
    title = models.CharField(max_length="255")
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Version"
        verbose_name_plural = "Versions"


class CategoryManager(models.Manager):
    """
    Category manager class. Adds functionality for querying
    categories that don't have children (simplesjop categories)
    """
    def get_query_set(self):
        return super(CategoryManager,
                self).get_query_set().order_by('sort_id')

    def parents(self):
        return self.get_query_set().filter(parent=None)


class Category(models.Model):
    """
    Category class represents a product category.
    """
    #objects = models.Manager()
    objects = CategoryManager()
    name = models.CharField(max_length=255)
    description = HTMLField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subcategories")
    slug = models.SlugField(max_length=255)
    image = models.ImageField("Image", upload_to="categories", max_length=200,
                              blank=True, null=True, help_text="Image will be resized to fit.")
    path = models.CharField(max_length=255, blank=True, null=True,
                            help_text="This field is automatically generated. If "
                            "this field is incorrect change the slug field.")
    sort_id = models.SmallIntegerField()

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categorieen"

    def __unicode__(self):
        return self.name

    def has_products(self):
        return bool(self.products.count())

    @models.permalink
    def get_absolute_url(self):
        # if self.has_products():
        #     if self.parent:
        #         args = {
        #             'category_slug': self.parent.slug,
        #             'subcategory_slug': self.slug,
        #         }
        #     else:
        #         args = {
        #             'category_slug': self.slug,
        #         }
        #     return('list-products', (), args)
        # else:
            return ('list-products', (), {'category_path': self.path})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.path or self.slug not in self.path:
            self.path = self.slug + '/'
            if self.parent:
                self.path = "%s%s/" % (self.parent.path, self.slug)
        super(Category, self).save(*args, **kwargs)


