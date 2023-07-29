from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from . models import *



# Create your views here.

def home(request):
    return HttpResponse(f"Hello, logged in user is = ,{request.user.first_name}")
# "Hi My name is {request.user}"

def register(request):
    #def & in between return
    if request.method == "POST":
        first_name=request.POST.get("fname",None)
        last_name=request.POST.get("lname",None)
        email=request.POST.get("email",None)
        password=request.POST.get("password", None)

        #save the data/register user in fucntions
        user = User.objects.create_user(username=email,email=email,first_name=first_name,last_name=last_name,password=password)
        return redirect("login")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=authenticate(request,**{"username":username,"password":password})
        print(user)
        if not user:
            print("User not found, please register")
        else:
            print("User found, logged in")
            print(request.user)
            auth_login(request,user)
            print(request.user)
            return redirect("create_invoice")
    
    return render(request, "login.html")

def create_invoice(request):
    if request.method == "POST":
        invoice_date=request.POST.get("invoice_date")
        invoice_number=request.POST.get("invoice_number")
        name=request.POST.get("customer_name")
        due_date=request.POST.get("due_date")
        

        counter=request.POST.get("count")

        for i in range(int(counter)):
            product_name1=request.POST.get("product_name"+str(i+1))
            qty1=request.POST.get("qty"+str(i+1))
            rate1=request.POST.get("rate"+str(i+1))
            total1=request.POST.get("total"+str(i+1))
            Invoice.objects.create(invoice_date=invoice_date,invoice_number=invoice_number,name=name,due_date=due_date,product_name1=product_name1,qty1=qty1,rate1=rate1,total1=total1,user=request.user)
        
    return render(request, "invoice.html")

def viewinvoice(request):
    invoices=Invoice.objects.all() # without any condition fetch all invoices
    #Invoice.objects.filter() # need to wirte arugment e.g. invoice =123 or cust name = sandeep
    context={"invoice1":invoices}
    print(invoices.first())

    return render(request,"viewinvoice.html",context)

def deleteinvoice(request,pk):
    
    Invoice.objects.filter(id=pk).delete()
    invoices=Invoice.objects.all()
    context={"invoice1":invoices}
    print(invoices.first())

    return render(request,"viewinvoice.html",context)