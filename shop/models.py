from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Banner(models.Model):
    title=models.CharField(max_length=200)
    desc=models.CharField(max_length=500)
    discount_1=models.IntegerField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],default=0.0)
    discount_2=models.IntegerField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],default=0.0)
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")
    desc=models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural='Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='Brands'

    def __str__(self):
        return self.title

# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size
class Size(models.Model):
    title=models.CharField(max_length=100)
    size_code=models.CharField(max_length=10)

    class Meta:
        verbose_name_plural='Sizes'

    def __str__(self):
        return self.title

# Product Model
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=400)
    sku=models.CharField(max_length=100)
    desc=models.TextField()
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    created_on = models.DateTimeField("created on", default=timezone.now)

    class Meta:
        verbose_name_plural='Products'

    def __str__(self):
        return self.title

#Product Attribute Pictures
class ProductAttributePictures(models.Model):
    name = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Images(models.Model):
    picture = models.ImageField(upload_to='shop/product_images', null=True, blank=True)  
    product = models.ForeignKey(ProductAttributePictures, on_delete=models.CASCADE)

# Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    discount=models.IntegerField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],default=0.0)
    quantity=models.PositiveIntegerField(default=0)
    sell_price=models.FloatField(null=True, validators=[MinValueValidator(0.0)])
    image=models.ForeignKey(ProductAttributePictures, on_delete=models.CASCADE, default=1)

    @property
    def sell_price(self):
        discount = 100 - self.discount
        discount_num = discount/100
        discount_num_b = float(discount_num)
        total = self.price*discount_num_b
        return round(total, 1)

    class Meta:
        verbose_name_plural='Product Attributes'

    def __str__(self):
        return self.product.title

    #def image_tag(self):
        #return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Product Tags
class ProductTag(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    tag_name=models.CharField(max_length=500)

    def __str__(self):
        return self.tag_name

# Order
status_choice=(
        ('processing','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )

class Cart(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    product_attribute=models.ForeignKey(ProductAttribute,on_delete=models.CASCADE)
    qty=models.PositiveBigIntegerField()

    def __str__(self):
        return self.product_attribute.product.title

# AddressBook
class Countries(models.Model):
    country_name=models.TextField()
    delivery_price=models.FloatField(default=25.0)

    def __str__(self):
        return self.country_name

# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    address_name=models.CharField(max_length=1000)
    country=models.ForeignKey(Countries, on_delete=models.CASCADE, default=1)
    town_or_city=models.CharField(max_length=1000)
    address=models.CharField(max_length=1000)
    postal_code=models.IntegerField()
    mobile=models.CharField(max_length=50,null=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.country.country_name

    class Meta:
        verbose_name_plural='AddressBook'

class CartOrder(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    total_amt=models.FloatField()
    address=models.ForeignKey(UserAddressBook, on_delete=models.CASCADE)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)
    paid_status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='Orders'

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'



 

