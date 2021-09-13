from wagtail.contrib.modeladmin.options import (
    ModelAdminGroup,
    ModelAdmin, 
    modeladmin_register
)

from .models import Category, Product


class CategoryAdmin(ModelAdmin):
    model                   = Category
    menu_label              = 'Category'  # ditch this to use verbose_name_plural from model
    menu_icon               = 'pilcrow'  # change as required
    menu_order              = 100  # will put in 3rd place (000 being 1st, 100 2nd)

# Now you just need to register your customised ModelAdmin class with Wagtail

class ProductAdmin(ModelAdmin):
    model                   = Product
    menu_label              = 'Product'  # ditch this to use verbose_name_plural from model
    menu_icon               = 'pilcrow'  # change as required


class CatalogGroupAdmin(ModelAdminGroup):
    menu_label = 'Catalog'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (CategoryAdmin, ProductAdmin)


modeladmin_register(CatalogGroupAdmin)
