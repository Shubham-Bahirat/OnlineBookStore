from django.shortcuts import render,redirect,HttpResponse
from django.template  import RequestContext
from  Admin_App.models import Category,Book,Payment_Card
from User_App.models import UserInfo,MyCart,orderInfo,ContactInfo
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime, date, timedelta

price = 0


def home(request):
    cats = Category.objects.all() # This Command fetch all items in the model 
    books = Book.objects.all()
    return render(request,"home.html",{"cats":cats,"books":books})

def showFilterBook(request,id):
    cats = Category.objects.all()
    books = Book.objects.all()  # This Command work like SQL Query "Select * from Book" 
    filter_books = Book.objects.filter(category = id)
    cnt = 0
    for book in filter_books:
        name = book.category
        cnt += 1
    return render(request,"home.html",{"cats":cats,"filter_books":filter_books,"books":books,"name":name})


def ViewDetails(request,id):
        cats = Category.objects.all()
        book = Book.objects.get(id=id) # Command to fetch the Unique perticular( Only one ) item in the model 
        cate = book.category_id
        books = Book.objects.filter(category_id = cate)
        r_book = []   # Command to fetch the filtered items more than one can be fecth
        for bk in books:
            if(book != bk):
                r_book.append(bk)   
                 
        return render(request,"ViewDetails.html",{"cats":cats,"book":book,"books":r_book})
   

def user_login(request):
    if(request.method == "GET"):
        return render(request,"user_login.html",{})
    else:
        uname = request.POST["uname"]
        psw = request.POST["psw"]
        try:
            user = UserInfo.objects.get(username = uname,password = psw)

            # If user is not found then show Message to user 
        except:
            messages.warning(request, 'Please Check your Username and Password')
            return redirect(user_login)
        
           # If user is found then show welcome Message 
        else:
            request.session["uname"] = uname
            messages.success(request, 'Mr/Mrs '+uname+' You have Successfully login')
            return redirect(home)

        
def logOut(request):
    request.session.clear() 
    return redirect(home)

def signUp(request):
    if(request.method == "GET"):
        return render(request,"signUp.html",{})
    else:
        uname = request.POST["uname"]
        email = request.POST["email"]
        psw = request.POST["psw"]
        try:
            user = UserInfo.objects.get(username = uname)

    #   except: If uname is not registered then register new user
        except:
            user = UserInfo(uname,email,psw)
            user.save()
            messages.success(request, 'Mr/Mrs '+uname+' You have Successfully Sign Up')
            return redirect(home)
    #   else:  If uname is already registered then register show message
        else:
            messages.error(request, '!!!  Username Already exist please try another username !!! ')
            return redirect(signUp)

def addTocart(request):
       #If uname in session ( user is login ) only then add to cart  
        if("uname" in request.session):
            user = UserInfo.objects.get(username = request.session["uname"])
            item = MyCart.objects.filter(user = request.session["uname"])
            print(item)
            bookid = request.POST["bid"] 
            book = Book.objects.get(id=bookid)
            qty = request.POST["qty"]
        #   try: try block check the item is present in cart or not 
        
            try:
                item = MyCart.objects.get(user=user,book=book)
        #   except:  if item is not present then add the item in cart
            except:
                cart = MyCart()
                cart.user = user
                cart.book = book
                cart.qty = qty
                cart.save() 
                messages.info(request, 'Success')       
        #  else : if item is present in cart then show message to add required quantity     
            else:
                messages.info(request, 'This Item You Have Already Added Please Add Required Quantity ')
            return redirect(showMycart)
    #   else:  uname not in session ( user is not login ) then redirect to login page 
        else:
            return redirect(user_login)

def showMycart(request):
    if(request.method =="GET"):
        # if form method is GET then fetch all cart items to show in user cart
        item = MyCart.objects.filter(user = request.session["uname"])
        cnt = len(item)
        Total_Price = 0
    #   for loop will count the cart items   
        for i in item: # In the 'item' there are diffrent objects like 'user,book' 
            request.session["cnt"] = cnt
            Total_Price += i.qty * i.book.price 
            # create session of Total Price 
            request.session["Total_Price"] = Total_Price
            if(cnt == 0):
                Total_Price += 0
        return render(request,"showMycart.html",{"items":item,"cnt":cnt})
#   else: Update and Remove Cart item 
    else:
        cart_id = request.POST["cart_id"]
        item = MyCart.objects.get(id=cart_id)
        action = request.POST["action"]
        if(action == "update"):
            qty = request.POST["qty"]
            item.qty = qty
            item.save()
        else:
            item.delete()
        return redirect(showMycart)
    
        
def Make_payment(request):
    Final_bill = 0
    if(request.method =="GET"):
        Total_Price = request.session["Total_Price"] 
        Final_bill = (Total_Price *0.88) 
        discount = int(Total_Price - (Final_bill))
    #   if Total Price is less than 5000 then add delivery charges '40 rupees' 
        if(int(Total_Price) < 5000):
            Final_amount = Final_bill + 100     
    #   if Total Price is grater than 5000 then No delivery charges 
        else:
            Final_amount = Final_bill
        request.session["Final_bill"] = Final_bill 

        user = UserInfo.objects.get(username =  request.session["uname"])
        address = user.address
       
        return render(request,"Make_payment.html",{"Final_bill":Final_amount,"discount":discount,"address":address})
#   else: if form method is post then fetch card details 
    else:
        cname = request.session["uname"]
        card_number = request.POST["cnumber"]
        cvv = request.POST["cvv"]
        expiry_date = request.POST["exdate"]
#   in try block check user card details with buyer card details
        try:
            customer = Payment_Card.objects.get(card_holder_name =cname,card_number=card_number,cvv=cvv,expiry=expiry_date)
    #   In eccept block user card details is not match with buyer card details then redirect to Make payment     
        except:
            return redirect(Make_payment)
    #  In else block if user card details is match with buyer card details then debit amount from user account 
    # and credit amount to Owner account
        else:
            owner = Payment_Card.objects.get(card_number='744855',cvv='455',expiry='10/2028')
            customer.balance -= float(request.session["Final_bill"])
            owner.balance += float(request.session["Final_bill"])
            customer.save()
            owner.save()

            myorder = orderInfo()
            user = UserInfo.objects.get(username=request.session["uname"])
            myorder.user  = user
            myorder.amount = request.session["Final_bill"]
            items = MyCart.objects.filter(user=user)
    
            details = ""
            for item in items:
                details += item.book.book_name+" , "
                item.delete()

             
            myorder.details= details
            myorder.save()
            request.session["Total_Price"] = 0
            messages.info(request, 'Order Placed')       
        return redirect(myOrder)


def buy_now(request):
    # If user want to buy the product direct means without adding to cart 
    if("uname" in request.session):
        if(request.method == "GET"):  # If form method is GET then show all Product Details
            bookid = request.GET["bid"]
            book = Book.objects.get(id = bookid)
            price = book.price
            name = book.book_name
            request.session["Price"] = price
            request.session["name"] = name
            user = UserInfo.objects.get(username =  request.session["uname"])
            address = user.address
            return render(request,"buy_now.html",{"book":book,"address":address})
        else: # If form method is POST then fetch Quntity of product and price 
              # then calculate total price, discount & delivery charges 
            qty = request.POST["qty"]
            request.session["qty"] = qty
            price = request.session["Price"] 
            t_price = int(qty) * int(price)
            discount = int(t_price * 0.08)
            delivery_c = int(qty) * 10
            amount_f = (t_price - discount) + delivery_c
            request.session["t_price"] = t_price
            request.session["discount"] =  discount 
            request.session["delivery_c"] =  delivery_c 
            request.session["amount_f"] = amount_f


            cname = request.session["uname"]
            card_number = request.POST["cnumber"]
            cvv = request.POST["cvv"]
            expiry_date = request.POST["exdate"]
            try: #   in try block check user card details with buyer card details
                customer = Payment_Card.objects.get(card_holder_name =cname,card_number=card_number,cvv=cvv,expiry=expiry_date)
            except: # In eccept block user card details is not match with buyer card details then redirect to Make payment  
                return redirect(Make_payment)
            else: #  In else block if user card details is match with buyer card details then debit amount from user account 
                  # and credit amount to Owner account
                owner = Payment_Card.objects.get(card_number='744855',cvv='455',expiry='10/2028')
                customer.balance -= float(amount_f)
                owner.balance += float(amount_f)
                customer.save()
                owner.save()

                myorder = orderInfo()
                user = UserInfo.objects.get(username=request.session["uname"])
                myorder.user  = user
                myorder.amount =  request.session["amount_f"]
                myorder.details = request.session["name"]
                myorder.save()
                return redirect(myOrder)
    else:
        return redirect(user_login)
    
        
def myOrder(request):
    item = orderInfo.objects.filter(user = request.session["uname"])
    #td = datetime.today()
    #delivery_date = td + timedelta(days=4)
    return render(request,"myOrder.html",{"items":item})   

def contact(request):
    if(request.method == "GET"):
        return render(request,"contact.html",{})
    else:
        name = request.POST["uname"]
        email = request.POST["email"]
        msg = request.POST["msg"]
        user = ContactInfo()
        user.name = name
        user.email = email
        user.massege = msg 
        user.save()
        return redirect(home)
    
def address(request):
    if(request.method == "GET"):
        user = UserInfo.objects.get(username =  request.session["uname"])
        address = user.address
        return render(request,"address.html",{"address":address})
    else:
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        zcode = request.POST["zipcode"]
        add = ""
        add += address+","+city+","+state+","+country+","+zcode

        user = UserInfo.objects.get(username = request.session["uname"])
        print("USER:",user)
        user.address = add
        user.save()   
        messages.success(request, 'You Address Successfully Updated')
        return redirect(home)

    
def search(request):
    if(request.method == "POST"):
        search = request.POST["search"]
        filter_books = Book.objects.filter( book_name  = search)
        filter_author = Book.objects.filter(author_name = search)
        print(filter_author,filter_books)
        return render(request,"search.html",{"src":search,"f_b":filter_books,"f_a":filter_author})