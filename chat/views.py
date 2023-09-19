from django.shortcuts import redirect, render
from chat.form import MemberForm, ProductForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect(login_view)
    groups = GroupChat.objects.all()
    
    context = {"groups":groups}
    return render(request, 'home.html', context)

def group_chat(request, id):
    if not request.user.is_authenticated:
        return redirect(login_view)
    
    group = GroupChat.objects.get(id=id)
    group_messages = group.groupmessage_set.all()
    print(group_messages)
    if request.method =="POST":
        message = request.POST.get("message")
        image = request.FILES.get("image")
        
        if image and 'image-btn' in request.POST:
            print(image)

            mess = GroupMessage.objects.create(image=image, is_image=True, sender = request.user, group=group)
            mess.save()
        if message and 'message-btn' in request.POST:
            mess = GroupMessage.objects.create(message=message, is_image=False, sender = request.user, group=group)
            mess.save()
            return redirect(group_chat, id)
            
    context = {"group_messages":group_messages}
    return render(request, 'group_chat.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email is not None and password is not None:
            user = authenticate(username= email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect(home)
            messages.error(request, "Enter corect credentials")
            return redirect(login_view)
        messages.error(request, "Enter corect credentials")
        return redirect(login_view)
    
    return render(request, 'login.html')

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            fullname = request.POST.get('fullname')

            if email is not None and password is not None and phone is not None:
                if User.objects.filter(username=email).exists():
                    messages.success(request, "User already exists")
                    return redirect(login_view)
                user = User.objects.create_user(username=email, password=password, email=email, first_name=fullname)
                user.save()
                messages.error(request, "Successfully registered, login")
                return redirect(login_view)
            return redirect(register_view)
        
    return render(request, 'register.html')


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect(login_view)
    user_groups = GroupChat.objects.filter(admin=request.user)
    if request.method =="POST" and 'productfm' not in request.POST:
        group_name = request.POST.get('group_name')
        
        gr = GroupChat.objects.create(name=group_name)
        gr.admin = request.user
        gr.save()
        messages.info(request, "Successfully added group")
        return redirect(user_profile)
    product_form = ProductForm()

    if request.method =="POST" and 'productfm'  in request.POST:
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Producr Saved Successfull")
            return redirect(user_profile)
        else:
            messages.error(request, "Producr not Successfull")
            return redirect(user_profile)

    context = {"user_groups":user_groups, "product_form":product_form, "products": Product.objects.all(), "orders": Orders.objects.all()}
    return render(request, 'user_profile.html', context)

def buy_product(request):
    product_id = request.POST.get("product_id")
    phone_number = request.POST.get("phone_number")

    if product_id and  phone_number:
        print(product_id, phone_number)
        oda = Orders.objects.create(user=request.user, product = Product.objects.get(id=product_id), phone_number=phone_number)
        messages.success(request, "Product bought successful")
        return redirect(user_profile)
    else:
        print("failed...........")
        

def add_group_member(request, id):
    group = GroupChat.objects.get(id=id)
    if not request.user.is_authenticated:
        return redirect(login_view)
    form = MemberForm(instance=group)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.info(request, "Successfully added members")
    
    context = {"form":form, "group":group}
    return render(request, 'add_group_member.html', context)

def logout_view(request):
    logout(request)
    return redirect(login_view)