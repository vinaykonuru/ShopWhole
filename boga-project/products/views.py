from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from decimal import *
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        products=Product.objects
        return render(request,'products/home.html',{'products':products})
    else:
        return render(request,'intro.html')
def detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/details.html',{'product':product})

def about(request):
    return render(request,'about.html')

@login_required(login_url='/accounts/signup')
def order(request,product_id):
    if request.method=='POST':
        product=get_object_or_404(Product,pk=product_id)
        if product.timerOver():
            return redirect('home')
        elif request.user not in product.customers.all(): #can only order once
            product.orders+=1
            product.customers.add(request.user)
            product.save()
            return redirect('home')
        else:
            return redirect('home')

@login_required(login_url='/accounts/signup')
def cart(request):
    user_cart=request.user.product_set.all()
    finalPrice=0
    for product in user_cart:
        finalPrice+=product.price
    return render(request, 'products/cart.html',{'cart':user_cart,'finalPrice':finalPrice})

@login_required(login_url='/accounts/signup')
def removeItem(request,product_id):
    if request.method=='POST':
        product=Product.objects.get(id=product_id)
        product.customers.remove(request.user)
        product.orders-=1
        return redirect('cart')

@login_required(login_url='/accounts/signup')
def checkout(request):
    user_cart=request.user.product_set.all()
    totalCost=0
    for product in user_cart:
        totalCost+=product.price
    tax=totalCost*Decimal('0.07')
    finalCost=totalCost+tax
    return render(request,'products/checkout.html',{'finalCost':round(finalCost,2),'tax':round(tax,2),'totalCost':round(totalCost,2)})
