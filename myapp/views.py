from django.shortcuts import render,redirect
from django.http import HttpResponseForbidden
from datetime import datetime, time
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from .forms import SignupForm,ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser
from django.core.mail import send_mail
from .models import MyUser,Product, Category
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.

def index(request):
    products=Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'index.html',context)

def user_index(request):
    products=Product.objects.all()
    context = {
        'products': products,
    }
    return render(request,'user-index.html',context)


@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login') 
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                if user.user_type == "Admin":
                    login(request, user)
                    return redirect('home')
                else:
                    login(request, user)
                    return redirect('user-index')
            else:
                handle_failed_login(request, username)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def handle_failed_login(request, username):
    user_key = f"failed_login_attempts_{username}"
    failed_attempts = request.session.get(user_key, 0)
    failed_attempts += 1
    request.session[user_key] = failed_attempts

    if failed_attempts >= 3:
        lock_account(request, username)
        send_lock_notification_email(username)

    messages.error(request, 'Invalid username or password. Please try again.')


def lock_account(request, username):
    user = MyUser.objects.get(username=username)
    user.is_locked = True
    user.save()
    messages.error(request, 'Account is locked. Please contact support.')


def send_lock_notification_email(username):
    subject = 'Account Lockout Notification'
    message = f"Dear {username}, your account has been locked due to multiple failed login attempts. " \
              f"If this was not you, please contact support."
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email for user in MyUser.objects.filter(username=username)]

    send_mail(subject, message, from_email, to_email)

# @csrf_exempt
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 print(user.user_type)
#                 if user.user_type == "Admin":
#                     login(request, user)    
#                     return redirect('home')
#                 else:
#                     login(request, user) 
#                     return redirect('user-index')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
@csrf_exempt
def product_detail(request, pk):
    product = Product.objects.get(id=pk)

    context = {
        'product': product,
    }
    return render(request,'product-detail.html',context)

@login_required
@csrf_exempt
def add_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.Admin = request.user
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    context = {
        "form":form
    }
    return render(request, 'add-product.html', context)

@login_required
@csrf_exempt
def update_product(request,pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return HttpResponseForbidden("Product does not exist.")

    if request.user != product.Admin:
        return HttpResponseForbidden("You don't have permission to update this product.")

    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            current_time = datetime.now().time()

            if form.cleaned_data.get('price') != product.price:
                original_price = product.price
                new_price = form.cleaned_data.get('price')
                price_change_percentage = ((new_price - original_price) / original_price) * 100
                if -10 <= price_change_percentage <= 10:
                    if (datetime.now().date() - product.last_price_update_date).days >= 1:
                        product.last_price_update_date = datetime.now().date()
                        form.save()
                        return redirect('home')
                    else:
                        return HttpResponseForbidden("You can update the price only once per day.")
                else:
                    return HttpResponseForbidden("Price change must be within -10% to +10%.")
            else:
                if current_time < datetime.strptime('11:00:00', '%H:%M:%S').time():
                    form.save()
                    return redirect('home')
                else:
                    return HttpResponseForbidden("Price update is allowed only before 11:00 AM.")
        else:
            form.save()
            return redirect('home')

    context = {
        "form": form
    }

    return render(request, 'update-product.html', context)
#     product = Product.objects.get(id=pk)

#     if request.user != product.Admin:
#         return HttpResponseForbidden("You don't have permission to update this product.")
#     form = ProductForm(instance=product)

#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             current_time = datetime.now().time()

#             if form.cleaned_data.get('price') != product.price:
#                     # Check if the last update was more than a day ago
#                 if (datetime.now().date() - product.last_price_update_date).days >= 1:
#                     product.last_price_update_date = datetime.now().date()
#                     form.save()
#                     return redirect('home')
#                 else:
#                     return HttpResponseForbidden("You can update the price only once per day.")
#             else:
#                 return HttpResponseForbidden("Price update is allowed only before 11:00 AM.")
#         else:
#             form.save()
#             return redirect('home')

#     context = {
#         "form":form
#     }

#     return render(request, 'update-product.html', context)



@login_required
@csrf_exempt
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('home')

def user_product_details(request, pk):
    product = Product.objects.get(id=pk)

    context = {
        'product': product,
    }
    return render(request,'user-product-details.html',context)


@login_required
@csrf_exempt
def update_price(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.user != product.Admin and not request.user.is_staff:
        return JsonResponse({'error': 'You don\'t have permission to update the price.'}, status=403)

    if request.method == 'POST':
        new_price = request.POST.get('new_price')

        try:
            new_price = float(new_price)
        except ValueError:
            return JsonResponse({'error': 'Invalid price format.'}, status=400)

        original_price = product.price
        price_change_percentage = ((new_price - original_price) / original_price) * 100

        if -10 <= price_change_percentage <= 10:
            if (datetime.now().date() - product.last_price_update_date).days >= 1:
                product.price = new_price
                product.last_price_update_date = datetime.now().date()
                product.save()
                return JsonResponse({'success': 'Price updated successfully.'})
            else:
                return JsonResponse({'error': 'You can update the price only once per day.'}, status=403)
        else:
            return JsonResponse({'error': 'Price change must be within -10% to +10%.'}, status=403)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)   