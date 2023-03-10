from django.contrib import admin
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,ProductTag,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Cart,Countries,ProductAttributePictures,Images
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

# Product Attribute
class ProductAttributeInline(admin.TabularInline):
	model = ProductAttribute

# Product Attribute
class ProductTagsInline(admin.TabularInline):
	model = ProductTag

class ImagesInline(admin.TabularInline):
	model=Images

class ProductAttributePicturesAdmin(admin.ModelAdmin):
	inlines=[ImagesInline]
admin.site.register(ProductAttributePictures, ProductAttributePicturesAdmin)
# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','product','price','discount','sell_price','quantity','color','size')
admin.site.register(ProductAttribute, ProductAttributeAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline,ProductTagsInline]
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

class CartOrderItemsInline(admin.StackedInline):
	def has_add_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	model = CartOrderItems
	form = CartOrderItemsInlineForm
#admin.site.register(CartOrderItems,CartOrderItemsAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	inlines = [CartOrderItemsInline]
	list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','address','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)


class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)

class CountriesAdmin(admin.ModelAdmin):
	list_display=('country_name','delivery_price')
admin.site.register(Countries,CountriesAdmin)
