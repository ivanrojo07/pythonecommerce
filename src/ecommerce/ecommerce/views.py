from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model

def login_page(request):
    form = LoginForm(request.POST or None)
    context ={
        'form':form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        print(request.user.is_authenticated)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user=authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            print(user)
            # context['form'] = LoginForm()
            return redirect("/login")
        else:
            print('Error')

    return render(request,"auth/login.html",context)
User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form':form
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user =User.objects.create_user(username,email,password)
        print(new_user)
    return render(request,"auth/register.html",context)

def home_page(request):
    context={
        "title":"HOME PAGE",
        "content":'pagina de bienvenida'
    }
    if request.user.is_authenticated:
        context['premium_content']="Premium content"
    return render(request,"home_page.html",context)
def about_page(request):
    context={
        "title":"ABOUT PAGE",
        "content":"pagina de acerca de"
    }
    return render(request,"home_page.html",context)
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context={
        "title":"CONTACT PAGE",
        "content":"pagina de contacto",
        "form":contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message":"Gracias por sus comentarios"},status=200)
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type='application/json')


    # if request.method == "POST":
    #     print(request.POST)
    return render(request,"contact/view.html",context)