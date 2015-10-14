from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
from django.db import models

class Cart(models.Model):
    
    created_date = models.DateTimeField(auto_now_add=True)
    checked_out = models.BooleanField(default=False)
    unique_identifier = models.CharField(max_length="120")
    
    def total_price(self):
        sum(item.total_price for item in self.items.all())

class ItemManager(models.Manager):
    
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            product = kwargs['product']
            del kwargs['product']
            kwargs['content_type'] = ContentType.objects.get_for_model(product.__class__)
            kwargs['object_id'] = product.pk
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    
    cart = models.ForeignKey('shoppingcart.Cart', related_name="items")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = ItemManager()
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price
    
    def increase(self, amount=1):
        self.quantity += amount
        self.save()
    
    def decrease(self, amount=1):
        if not self.quantity <= amount:
            self.quantity -= amount
            self.save()
        else:
            self.delete()
    
    class AlreadyExists(Exception):
        pass
    
    class ProductClassUndefined(Exception):
        pass

class ItemInline(admin.StackedInline):
    model = Item

class CartAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

admin.site.register(Cart, CartAdmin)
