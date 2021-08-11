from django.contrib import admin
from django.db import models
from django.utils.html import mark_safe
from main_app.models import Address, Oreder_Detail, Product_detail, Product_Img, Design_Img, Design, Profile, user_feedback
# Register your models here.


def get_picture_preview(obj):
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        return mark_safe("""<img src="{src}" style="max-width: 200px; max-height: 200px;" /></a>""".format(
            src=obj.image.url
        ))
    return ("(choose a picture and save and continue editing to see the preview)")


get_picture_preview.allow_tags = True
get_picture_preview.short_description = ("Picture Preview")


class DesignImgAdmin(admin.StackedInline):
    model = Design_Img
    extra = 0


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    inlines = [DesignImgAdmin]

    class Meta:
        model = Design


@admin.register(Design_Img)
class DesignImgAdmin(admin.ModelAdmin):
    pass


class ProducImgAdmin(admin.StackedInline):
    model = Product_Img
    extra = 1
    fields = ['image', get_picture_preview]
    readonly_fields = [get_picture_preview, ]


@admin.register(Product_detail)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProducImgAdmin]
    list_display = ('name', 'price', 'discount',
                    'best_for', 'design_pattern', 'date_time',)
    list_per_page = 6

    class Meta:
        model = Product_detail


@admin.register(Product_Img)
class ProducImgAdmin(admin.ModelAdmin):
    pass


@admin.register(Oreder_Detail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'pro_name', 'Product_quantity',
                    'Pro_price', 'size_name', 'total_price', 'date_time')
    readonly_fields = ['user_name', 'address', 'review', 'pro_name', 'Product_quantity',
                       'Pro_price', 'size_name', 'size_detail', 'total_price', 'date_time']
    exclude = ('size_id', 'address_id', 'design_id', 'Product_Id',)
    list_per_page = 10
    search_fields = ('user_name', 'pro_name', 'Product_quantity',
                     'Pro_price', 'size_name', 'total_price', 'date_time', 'size_id', 'address_id', 'design_id', 'Product_Id',)
    list_filter = ('user_name', 'pro_name', 'Product_quantity',
                   'size_name', 'date_time',)


@admin.register(user_feedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_filter = ('product', 'stiching_quality',
                   'product_quality', 'fitting_quality', 'liked', 'date_time',)
    search_fields = ('product', 'stiching_quality',
                     'product_quality', 'fitting_quality', 'liked', 'date_time',)
    list_filter = ('product', 'stiching_quality',
                   'product_quality', 'fitting_quality', 'liked', 'date_time',)
    list_display = ('product', 'stiching_quality',
                    'product_quality', 'fitting_quality', 'liked', 'date_time',)
    list_per_page = 10

# admin.site.register(Profile)
# admin.site.register(Address)
