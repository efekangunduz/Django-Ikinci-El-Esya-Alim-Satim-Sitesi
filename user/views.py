from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
from home.models import UserProfile
from order.models import Order, OrderProduct
from product.models import Category, Comment, Product
from user.forms import UserUpdateForm, ProfileUpdateForm, ProductForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile
               }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relation with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarılı bir şekilde güncellendi.')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Hata! <br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'category': category})


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorumunuz başarı ile silindi.')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
    }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')
def orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')
def addproduct(request):
    product_form = ProductForm(request.POST, request.FILES)
    if request.method == 'POST':
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Your product added!')
            return HttpResponseRedirect('/user/addproduct')
    else:
        category = Category.objects.all()
        product = Product.objects.all()
        context = {
            'category': category,
            'product_form': product_form,
            'product': product,
        }
        return render(request, 'user_addproduct.html', context)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


def products(request):
    category = Category.objects.all()
    current_user = request.user
    products = Product.objects.filter(ekleyen_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
        'products': products,
    }
    return render(request, 'user_products.html', context)


def deleteproduct(request,id):
    current_user = request.user
    Product.objects.filter(id=id, ekleyen_id=current_user.id).delete()
    messages.success(request, 'Ürün başarı ile silindi.')
    return HttpResponseRedirect('/user/products')