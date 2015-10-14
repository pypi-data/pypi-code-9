from django.contrib import admin

from .models import Product, Category, ProductBase


class ProductVersionInline(admin.TabularInline):
    """
    Displays an inline of products in the product admin page.
    """
    model = Product


class ProductAdmin(admin.ModelAdmin):
    """
    Admin settings for Products
    """
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('title', 'category_path', 'sort_id', 'image_thumbnail',)
    search_field = ('title', 'name', 'description',)
    inlines = [ProductVersionInline]
    list_editable = ('sort_id',)

    def category_path(self, obj):
        return obj.category.path
    category_path.admin_order_field = 'category__path'


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin settings for Categories.
    """
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('path',)
    list_display = ('name', 'path', 'sort_id')
    list_editable = ('sort_id',)


admin.site.register(ProductBase, ProductAdmin)
admin.site.register(Category, CategoryAdmin)