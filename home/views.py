from django.shortcuts import render,HttpResponse,redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime,timedelta,date
from .models import IssueBook, UserExtend,AddBook,ReturnBook,AddStudent
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
def index(request):
    return render(request,'index.html')
def ourbooks(request):
    Book = AddBook.objects.all()
    return render(request,'ourbooks.html',{'Book':Book})
    # return render(request,'ourbooks.html')
def aboutus(request):
    return render(request,'aboutus.html')
def allbooks(request):
    Book = AddBook.objects.all()
    return render(request,'viewallbooks.html',{'Book':Book})

def contactus(request):
    return render(request,'contactus.html')
def staff(request):
    return render(request,'staff.html')
def stafflogin(request):
    if request.session.has_key('is_logged'):
        return redirect('dashboard')
    return render(request,'stafflogin.html')
def staffsignup(request):
    return render(request,'staffsignup.html')
def dashboard(request):
    if request.session.has_key('is_logged'):
        Book = AddBook.objects.all()
        return render(request,'dashboard.html',{'Book':Book})
    return redirect('stafflogin')
def addbook(request):
    Book = AddBook.objects.all()
    return render(request,'addbook.html',{'Book':Book})
def SignupBackend(request):
    if request.method =='POST':
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email = request.POST["email"]
            phone=request.POST['phone']
            password=request.POST['password']
            userprofile = UserExtend(phone=phone)
            if request.method == 'POST':
                try:
                    UserExists = User.objects.get(username=request.POST['uname'])
                    messages.error(request," Username already taken, Try something else!!!")
                    return redirect("staffsignup")    
                except User.DoesNotExist:
                    if len(uname)>10:
                        messages.error(request," Username must be max 15 characters, Please try again")
                        return redirect("staffsignup")
            
                    if not uname.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")
                        return redirect("staffsignup")
            
            # create the user
            user = User.objects.create_user(uname, email, password)
            user.first_name=fname
            user.last_name=lname
            user.email = email
            user.save()
            userprofile.user = user
            userprofile.save()
            messages.success(request," Your account has been successfully created")
            return redirect("stafflogin")
    else:
        return HttpResponse('404 - NOT FOUND ')
def LoginBackend(request):
    if request.method =='POST':
        loginuname = request.POST["loginuname"]
        loginpassword=request.POST["loginpassword"]
        RegisteredUser = authenticate(username=loginuname, password=loginpassword)
        if RegisteredUser is not None:
            dj_login(request, RegisteredUser)
            request.session['is_logged'] = True
            RegisteredUser = request.user.id 
            request.session["user_id"] = RegisteredUser
            messages.success(request, " Successfully logged in")
            return redirect('dashboard')
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    return HttpResponse('404-not found')
def AddBookSubmission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            bookid = request.POST["bookid"]
            bookname = request.POST["bookname"]
            subject = request.POST["subject"]
            category=request.POST["category"]
            add = AddBook(user = user1,bookid=bookid,bookname=bookname,subject=subject,category=category)
            add.save()
            Book = AddBook.objects.all()
            return render(request,'dashboard.html',{'Book':Book})
    return redirect('/')
def deletebook(request,id):
    if request.session.has_key('is_logged'):
        AddBook_info = AddBook.objects.get(id=id)
        AddBook_info.delete()
        return redirect("dashboard")
    return redirect("login") 
def bookissue(request):
    return render(request,'bookissue.html')
def returnbook(request):
    return render(request,'returnbook.html')
def HandleLogout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('dashboard')
def issuebooksubmission(request):
       if request.method=='POST':
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            studentid=request.POST['studentid']
            book1=request.POST['book1']
            store=AddBook.objects.filter(bookid=book1)
            def get_category(addbook):
                if addbook.category=="Not-Issued":
                    addbook.category="Issued"
                    obj= IssueBook(user=user1,studentid=studentid,book1=book1)
                    obj.save()
                    addbook.save()
                else:
                    messages.error(request," Book already issued !!!")
            category_list=list(set(map(get_category,store)))         
            Issue=IssueBook.objects.all()
            return render(request,'bookissue.html',{'Issue':Issue})
       return redirect('/')
def returnbooksubmission(request):
    if request.method=='POST':
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            bookid2=request.POST['bookid2']
            store1=AddBook.objects.filter(bookid=bookid2)
            def return_book(returnbook):
                if returnbook.category=="Issued":
                    returnbook.category="Not-Issued"
                    obj1=ReturnBook(user=user1,bookid2=bookid2)
                    obj=IssueBook.objects.filter(book1=bookid2)
                    obj.delete()
                    obj1.save()
                    returnbook.save()
                else:
                    messages.error(request," Book not  issued !!!")
            returncategorylist=list(set(map(return_book,store1)))
            Return= ReturnBook.objects.all()
            return render(request,'returnbook.html',{'Return':Return})
    return redirect('/')
def Search(request):
    if request.session.has_key('is_logged'):
        query2=request.GET["query2"]
        Book=AddBook.objects.filter(bookid__icontains=query2)
        params={'Book':Book}
        return render(request,'dashboard.html',params)
    return redirect("login") 
def editbookdetails(request,id):
    if request.session.has_key('is_logged'):
        Book = AddBook.objects.get(id=id)
        return render(request,'editdetails.html',{'Book':Book})
    return redirect('login')

def updatedetails(request,id):
    if request.session.has_key('is_logged'):
        if request.method=="POST":
                add=AddBook.objects.get(id=id)
                add.bookid=request.POST["bookid"]
                add.bookname=request.POST["bookname"]
                add.subject=request.POST["subject"]
                add.ContactNumber=request.POST['category']
                add.save()
                return redirect("dashboard")
    return redirect('login')

def addstudent(request):
    if request.session.has_key('is_logged'):
       return render(request,'addstudent.html')
    return redirect ('login')

def viewstudents(request):
    if request.session.has_key('is_logged'):
        Student=AddStudent.objects.all()
        return render(request,'viewstudents.html',{'Student':Student})
    return redirect('stafflogin')

def Searchstudent(request):
    if request.session.has_key('is_logged'):
        query3=request.GET["query3"]
        Student=AddStudent.objects.filter(studentid__icontains=query3)
        params={'Student':Student}
        return render(request,'viewstudents.html',params)
    return redirect("stafflogin") 

def addstudentsubmission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            sname = request.POST["sname"]
            studentid = request.POST["studentid"]
            add = AddStudent(user = user1,sname=sname,studentid=studentid)
            add.save()
            Student = AddStudent.objects.all()
            return render(request,'viewstudents.html',{'Student':Student})
    return redirect('/')

def viewissuedbook(request):
    if request.session.has_key('is_logged'):
        issuedbooks=IssueBook.objects.all()
        lis=[]
        li=[]
        for books in issuedbooks:
            issdate=str(books.issuedate.day)+'-'+str(books.issuedate.month)+'-'+str(books.issuedate.year)
            expdate=str(books.expirydate.day)+'-'+str(books.expirydate.month)+'-'+str(books.expirydate.year)
            #fine calculation
            days=(date.today()-books.issuedate)
            d=days.days
            fine=0
            if d>15:
                day=d-15
                fine=day*10
            print(d)

            book=list(AddBook.objects.filter(bookid=books.book1))
            students=list(AddStudent.objects.filter(studentid=books.studentid))
            print(book)
            print(students)
            i=0
            for k in book:
                print(li)
                t=(students[i].sname,students[i].studentid,book[i].bookname,book[i].subject,issdate,expdate,fine)
                print(t)
                i=i+1
                lis.append(t)
                print(lis)

        return render(request,'viewissuedbook.html',{'lis':lis})
    return redirect('/')

