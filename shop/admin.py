from django.contrib import admin
from .models import Banner,Category,Brand,Color,Size,ProductPicture,Product,ProductAttribute,ProductTag,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Cart
from django import forms

# admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Size)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductPictureInline(admin.TabularInline):
    model = ProductPicture

# Product Attribute
class ProductAttributeInline(admin.TabularInline):
	model = ProductAttribute

# Product Attribute
class ProductTagsInline(admin.TabularInline):
	model = ProductTag

# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color','size')
admin.site.register(ProductAttribute, ProductAttributeAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPictureInline, ProductAttributeInline,ProductTagsInline]
    list_display=('id','title','category','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','product_attribute','qty')
admin.site.register(Cart,CartAdmin)

class CartOrderItemsInlineForm(forms.ModelForm):
	model = CartOrderItems

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for f in self.fields:
			self.fields[f].widget.attrs['readonly'] = 'readonly'

class CartOrderItemsInline(admin.TabularInline):
	model = CartOrderItems
	form = CartOrderItemsInlineForm
#admin.site.register(CartOrderItems,CartOrderItemsAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	inlines = [CartOrderItemsInline]
	list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)


class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)