from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from django.db.models import Q
from django.utils import timezone
import datetime
from django.shortcuts import render, get_object_or_404, redirect





# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
def viewusers(request):
    users=Register.objects.filter(usertype='user')
    print(users)
    return render(request,'viewusers.html',{'user':users})
def edit(request):
    return render(request,'edit.html')
def productview(request):
    return render(request,'viewproducts.html')
def cart(request):
    return render(request,'cart.html')

def user_login(request):
    form1=LoginForm(request.POST,request.FILES)
    if request.method == 'POST':
        if form1.is_valid():
            username=form1.cleaned_data['username']
            password=form1.cleaned_data['password']
            print(username,password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)  
                data=Register.objects.get(username=username)
                if data.is_superuser:
                    data.usertype ='admin'
                    data.save()
                request.session['ut'] = data.usertype
                
                return redirect('/1') 
            else:
                
                messages.error(request, "Invalid username or password!")
                return redirect('/3')
                     
    else:
        form1 = LoginForm()
    
    return render(request, "login.html", {"form": form1})

def register(request):
    form2=RegiterForm(request.POST,request.FILES)
    if request.method == 'POST':
        if form2.is_valid():
            # name1=request.POST['first_name']
            # name2=request.POST['last_name']
            # name3=request.POST['contact']
            # name4=request.POST['email']
            # print(name1)
            # print(name2)
            # print(name3)
            # print(name4)
            
            # Register.objects.create_user(username=name1,last_name=name2,contact=name3,email=name4)
            k=form2.save(commit=False)
            
            k.usertype="user"
            k.password=make_password(form2.cleaned_data['password'])
            k.save()
            return redirect('/3')
    else:
        form2=RegiterForm()
    return render(request,'register.html',{'form':form2})


def delete_user(request, user_id):
   user=Register.objects.get(id=user_id)
   user.delete()
   return redirect('/5') 

def edit_user(request, user_id):
    user=Register.objects.get(id=user_id)
    if request.method == 'POST':
        form1 = EditForm(request.POST, instance=user)
        if form1.is_valid():
            form1.save()
            return redirect('/5')
    else:
        form1 = EditForm(instance=user)
    
    return render(request, 'register.html', {'form': form1})

def logout_view(request):
    logout(request)
    request.session.pop('ut', None) 
    return redirect('/1') 

def products(request):
    

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/8') 
    else:
        form = ProductForm()
    products = Product.objects.all()
    return render(request, 'products.html', {'form': form, 'products': products})


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('/8')  


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/8')
    else:
        form = ProductForm(instance=product)
    
    products = Product.objects.all()
    return render(request, 'products.html', {'form': form, 'products': products, 'editing': True, 'editing_id': product.id})

def view_products(request):
    products = Product.objects.all().prefetch_related('orders')
   
    cart = request.session.get('cart', {})
    cart_product_ids = [int(pid) for pid in cart.keys()]

    for product in products:
        product.reviews = Order.objects.filter(
            product=product,
            status='Delivered',
            feedback__isnull=False
        ).select_related('user').order_by('-ordered_at')

    return render(request, 'viewproducts.html', {
        'products': products,
        'cart_product_ids': cart_product_ids
        
    })
    
 
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('/9')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')

       
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    default_quantity = cart.get(str(product_id), 1)
    subtotal = product.price * default_quantity
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        address = request.POST.get('address')

        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            address=address
        )
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        return redirect('view_orders')

       

    return render(request, 'buy.html', {
    'product': product,
    'default_quantity': default_quantity,
    'subtotal': subtotal
     })


def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'order.html', {'orders': orders})



def get_status_priority(status):
    priority = {
        'Placed': 0,
        'Shipped': 1,
        'Delivered': 2,
        'Cancelled': 3
    }
    return priority.get(status, 4)

def view_bookings(request):
    orders = Order.objects.select_related('product', 'user').all()

    # Sort first by status priority, then by ordered_at descending (newest first)
    orders = sorted(
        orders,
        key=lambda o: (get_status_priority(o.status), -o.ordered_at.timestamp())
    )

    pending_count = Order.objects.filter(status__in=['Placed', 'Shipped']).count()
    cancelled_count = Order.objects.filter(status='Cancelled').count()

    context = {
        'orders': orders,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
    }
    return render(request, 'bookings.html', context)
   
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()
    
    return redirect('view_orders')


def checkout_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        address = request.POST.get('address')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                address=address
            )

        # Clear cart
        request.session['cart'] = {}

        return redirect('view_orders')  # Or thank-you page
    return redirect('view_cart')

def buy_all_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')  # nothing to buy

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'buy_all.html', {
        'cart_items': cart_items,
        'total': total
    })
    
def confirm_buy_all(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        address = request.POST.get('address')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            quantity_input_name = f'quantities_{product_id}'
            quantity = int(request.POST.get(quantity_input_name, 1))
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                address=address
            )

        request.session['cart'] = {}  # clear cart
        return redirect('view_orders')
    return redirect('buy_all_view')   

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        return redirect('view_bookings')

    return render(request, 'update_status.html', {'order': order})



def submit_feedback(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.rating = int(request.POST.get('rating'))
        order.feedback = request.POST.get('feedback')
        order.feedback_at = datetime.datetime.today() 
        order.save()
    return redirect('view_orders')




def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('add_category')  # Refresh the page
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm()
    return render(request, 'products.html', {'form': form})
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart = request.session.get('cart', {})
                cart[str(product_id)] = quantity
                request.session['cart'] = cart
        except ValueError:
            pass
    return redirect('view_cart')



def view_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    cart = request.session.get('cart', {})
    cart_product_ids = [int(pid) for pid in cart.keys()]

    # Filter parameters
    selected_category = request.GET.get('category')
    price_range = request.GET.get('price_range')

    if selected_category and selected_category != 'all':
        products = products.filter(category=selected_category)

    if price_range:
        if '+' in price_range:  # e.g., "5001+"
            try:
                min_price = int(price_range.replace('+', ''))
                products = products.filter(price__gte=min_price)
            except ValueError:
                pass  # Handle or log error if needed
        else:
            try:
                min_price, max_price = map(int, price_range.split('-'))
                products = products.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                pass  # Handle or log error if needed    

    # Attach reviews to products
   # Attach reviews to products (latest first)
    for product in products:
        product.reviews = Order.objects.filter(
            product=product,
            status='Delivered',
        feedback__isnull=False
        ).select_related('user').order_by('-feedback_at')  # newest first

    return render(request, 'viewproducts.html', {
        'products': products,
        'cart_product_ids': cart_product_ids,
        'categories': categories,
        'selected_category': selected_category,
        'price_range': price_range,
    })
    
def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
    return redirect('add_category')