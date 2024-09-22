from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from datetime import datetime,timedelta
class UserExtend(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField()
    def __str__(self):
       return self.user.username
class AddBook(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    bookid=CharField(max_length=10)
    bookname=CharField(max_length=50)
    subject=CharField(max_length=20)
    category= models.CharField(max_length = 10)
    def __str__(self):
        return str(self.bookname)+"["+str(self.bookid)+']'
def expiry():
    return datetime.today() + timedelta(days=15)
class IssueBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    studentid=CharField(max_length=20)
    book1=models.CharField(max_length=20)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=expiry)
    def __str__(self):
        return self.studentid
class ReturnBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bookid2=models.CharField(max_length=20)
class AddStudent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    sname=models.CharField(max_length=30)
    studentid=models.CharField(max_length=20)
    def __str__(self):
        return self.sname+'['+str(self.studentid)+']'