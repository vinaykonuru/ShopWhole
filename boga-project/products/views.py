from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
# Create your views here.
def home(request):
    products=Product.objects
    return render(request,'products/home.html',{'products':products})

def detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/details.html',{'product':product})

@login_required(login_url='/accounts/signup')
def order(request,product_id):
    if request.method=='POST':
        product=get_object_or_404(Product,pk=product_id)

        if request.user not in product.customers.all(): #can only order once
            product.orders+=1
            product.customers.add(request.user)
            product.save()
            return redirect('home')
        else:
            return redirect('home')
def cart(request):
    user_cart=request.user.product_set.all()
    return render(request, 'products/cart.html',{'cart':user_cart})
