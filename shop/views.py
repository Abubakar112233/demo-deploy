from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Brand,Product,ProductAttribute,ProductPicture,ProductTag,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Color,Size,Cart
from blog.models import Article
from users.models import Currency
from django.contrib import messages
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import ReviewAdd,AddressBookForm,ProfileForm,ContactForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
# Home Page
def home(request):
	if 'currencyselected' in request.session:
		pass
	else:
		# del request.session['cartdata']
		selected_currency={}
		selected_currency={		
			'currency':Currency.objects.first().id,
		}
		request.session['currencyselected']=selected_currency

	banners=Banner.objects.all().order_by('-id')
	data=Product.objects.filter(is_featured=True).filter(status=True).order_by('-id')[:8]
	category=Category.objects.all()
	article = Article.objects.all()[:3]
	return render(request,'products/index.html',{'data':data,'banners':banners,'category':category,'article':article,'selected_currency':request.session['currencyselected']})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'categories/category_list.html',{'data':data})

# Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brands/brand_list.html',{'data':data})

# Product List
def product_list(request):
	total_data=Product.objects.count()
	data=Product.objects.all().order_by('-id')[:3]
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'products/product_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)

def product_discount(request,banner_id):
	discount_1=Banner.objects.get(id=banner_id).discount_1
	discount_2=Banner.objects.get(id=banner_id).discount_2
	allProducts=ProductAttribute.objects.filter(discount__gte=discount_1,discount__lte=discount_2).order_by('-id')
	return render(request, 'products/product_discount.html', {'data':allProducts})

# Product List According to Category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	return render(request,'categories/category_product_list.html',{
			'data':data,
			'category':category
			})

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'categories/category_product_list.html',{
			'data':data,
			})

# Product Detail
def product_detail(request,slug,id):
	product=Product.objects.get(id=id)
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	colors=ProductAttribute.objects.filter(product=product).filter(quantity__gt=0).values('color__id','color__title','color__color_code').distinct()
	sizes=ProductAttribute.objects.filter(product=product).filter(quantity__gt=0).values('size__id','size__title','size__size_code','price','discount','color__id','image').distinct()
	product_pictures=ProductPicture.objects.filter(Product=product)
	product_tags=ProductTag.objects.filter(product=product)
	reviewForm=ReviewAdd()

	# Check
	canAdd=True
	if request.user.is_authenticated:
		reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'products/product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'product_pictures':product_pictures,'product_tags':product_tags})

# Product Detail
def product_attribute_detail(request,id):
	data = ProductAttribute.objects.get(id=id)
	product=ProductAttribute.objects.get(id=id).product
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	product_tags=ProductTag.objects.filter(product=product)
	reviewForm=ReviewAdd()

	# Check
	canAdd=True
	if request.user.is_authenticated:
		reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'products/product_attribute_detail.html',{'datas':product,'data':data,'related':related_products,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'product_tags':product_tags})

# Search
def search(request):
	q=request.GET['q']
	data=Product.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})

# Filter Data
def filter_data(request):
	user=request.user
	request=request
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=ProductAttribute.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(price__gte=minPrice)
	allProducts=allProducts.filter(price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(product__category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(product__brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-filtered-list.html',{'data':allProducts, 'request':request, 'user':user})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	user=request.user
	request=request
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data,'request':request, 'user':user})
	return JsonResponse({'data':t}
)

# Add to cart
def add_to_cart(request):
	if request.user.is_authenticated:
		product_id = ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0]
		user = request.user
		p_qty = request.GET['qty'] 

		if Cart.objects.filter(product_attribute = product_id).filter(user=user).exists():
			cart = Cart.objects.get(product_attribute = product_id, user=user)
			cart.qty = p_qty
			cart.save()

			return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

		else:	
			Cart.objects.create(
				user = user,
				product_attribute = product_id,
				qty = p_qty
			)
			
			messages.success(request, "Item Added To Cart")
			return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
			

	else:
		# del request.session['cartdata']
		cart_p={}
		cart_p[str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id)]={		
			'image':request.GET['image'],
			'title':request.GET['title'],
			'qty':request.GET['qty'],
			'color':request.GET['color'],
			'size':request.GET['size'],
			'price':request.GET['price'],
		}

		if 'cartdata' in request.session:
			if str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id) in request.session['cartdata']:
				cart_data=request.session['cartdata']
				cart_data[str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id)]['qty']=int(cart_p[str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id)]['qty'])
				cart_data.update(cart_data)
				request.session['cartdata']=cart_data
			else:
				cart_data=request.session['cartdata']
				cart_data.update(cart_p)
				request.session['cartdata']=cart_data
		else:
			request.session['cartdata']=cart_p
		messages.success(request, "Item Added To Cart")
		return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
\
# Add to cart
def add_to_cart_attribute(request):
	if request.user.is_authenticated:
		product_id = ProductAttribute.objects.get(id=request.GET['id']) 
		user = request.user
		p_qty = request.GET['qty'] 

		if Cart.objects.filter(product_attribute = product_id).filter(user=user).exists():
			cart = Cart.objects.get(product_attribute = product_id, user=user)
			cart.qty = p_qty
			cart.save()

			return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

		else:	
			Cart.objects.create(
				user = user,
				product_attribute = product_id,
				qty = p_qty
			)
			
			messages.success(request, "Item Added To Cart")
			return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
			

	else:
		# del request.session['cartdata']
		cart_p={}
		cart_p[str(ProductAttribute.objects.get(id=request.GET['id']))]={		
			'qty':request.GET['qty'],
		}

		if 'cartdata' in request.session:
			if str(ProductAttribute.objects.get(id=request.GET['id'])) in request.session['cartdata']:
				cart_data=request.session['cartdata']
				cart_data[str(ProductAttribute.objects.get(id=request.GET['id']))]['qty']
				cart_data.update(cart_data)
				request.session['cartdata']=cart_data
			else:
				cart_data=request.session['cartdata']
				cart_data.update(cart_p)
				request.session['cartdata']=cart_data
		else:
			request.session['cartdata']=cart_p
		messages.success(request, "Item Added To Cart")
		return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

def cart_list(request):
	request = request
	user=request.user
	if request.user.is_authenticated:
		user=request.user
		total_amt=0
		cart_items = Cart.objects.filter(user=user)
		for item in cart_items:
			total_amt+=item.qty*item.product_attribute.sell_price
		return render(request, 'cart/cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt,'cart_items':cart_items,'request':request, 'user':user})
	else:
		total_amt=0
		if 'cartdata' in request.session:
			for p_id,item in request.session['cartdata'].items(): 
				total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
			return render(request, 'cart/cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'request':request, 'user':user})
		else:
			return render(request, 'cart/cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt,'request':request, 'user':user})


# Delete Cart Item
def delete_cart_item(request):
	if request.user.is_authenticated:
		p_id=int(str(request.GET['id']))
		cart = Cart.objects.get(id=p_id)
		cart.delete()


		cart_items = Cart.objects.all()
		
		total_amt=0
		for item in cart_items:
			total_amt+=int(item.qty)*float(item.product_attribute.sell_price)
		messages.error(request, "Item Deleted from Cart")
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'cart_items':cart_items})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

	else:
		p_id=str(request.GET['id'])
		if 'cartdata' in request.session:
			if p_id in request.session['cartdata']:
				cart_data=request.session['cartdata']
				del request.session['cartdata'][p_id]
				request.session['cartdata']=cart_data
		total_amt=0
		for p_id,item in request.session['cartdata'].items(): 
			total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
		messages.error(request, "Item Deleted from Cart")
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# Delete Cart Item
def update_cart_item(request):
	if request.user.is_authenticated:	
		request = request
		user=request.user
		p_id=int(str(request.GET['id']))
		p_qty=int(request.GET['qty'])
		cart = Cart.objects.get(id=p_id)
		cart.qty = p_qty
		cart.save()


		cart_items = Cart.objects.filter(user=user)
		
		total_amt=0
		for item in cart_items:
			total_amt+=int(item.qty)*float(item.product_attribute.sell_price)
		
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'cart_items':cart_items,'request':request, 'user':user})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

	else:
		request = request
		user=request.user
		p_id=str(request.GET['id'])
		p_qty=request.GET['qty']
		if 'cartdata' in request.session:
			if p_id in request.session['cartdata']:
				cart_data=request.session['cartdata']
				cart_data[str(request.GET['id'])]['qty']=p_qty
				request.session['cartdata']=cart_data
		total_amt=0
		for p_id,item in request.session['cartdata'].items(): 
			total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'request':request, 'user':user})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# Checkout
@login_required
def checkout(request):
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items(): 
			totalAmt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
		# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items(): 
			total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=ProductAttribute.objects.get(id=p_id).sell_price,
				total=float(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
				)
			# End
		# Process Payment
		host = request.get_host()
		paypal_dict = {
		    'business': settings.PAYPAL_RECEIVER_EMAIL,
		    'amount': total_amt,
		    'item_name': 'OrderNo-'+str(order.id),
		    'invoice': 'INV-'+str(order.id),
		    'currency_code': 'USD',
		    'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		    'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
		    'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
		}
		form = PayPalPaymentsForm(initial=paypal_dict)
		address=UserAddressBook.objects.filter(user=request.user,status=True).first()
		return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form':form,'address':address})

@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Save Review
def save_review(request,pid):
	product=Product.objects.get(pk=pid)
	user=request.user
	review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# Contact
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'name': form.cleaned_data['name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'abubakarlawan112@gmail.com', ['abubakarlawan112@gmail.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("contact")
      
	form = ContactForm()
	return render(request, 'contact.html', {'form':form})

# User Dashboard
import calendar
def my_dashboard(request):
	orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		messages.error(request, "Item Already in Wishlist")
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		messages.success(request, "Item Added To Wishlist")
		data={
			'bool':True
		}
	return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})

# My Reviews
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews})

# My AddressBook
def my_addressbook(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})