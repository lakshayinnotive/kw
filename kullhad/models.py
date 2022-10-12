from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class LoginData(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.CharField(max_length=80, default="")
#     mobile_no = models.CharField(max_length=20, default="")
#     city = models.CharField(max_length=60)
#     location = models.CharField(max_length=100, default="")
#     ip_address = models.CharField(max_length=50, default="")

#     def _str_(self):
#         return self.username

# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     auth_token = models.CharField(max_length=100)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username



class Userdata(models.Model):
    id = models.AutoField
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=500)
    username = models.CharField(max_length=50, primary_key=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    mobile_no = models.IntegerField
    city = models.CharField(max_length=60)

    email_token = models.CharField(max_length=200, default="_")

    def _str_(self):
        return self.username

class LoginData(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=80, default="")
    mobile_no = models.CharField(max_length=20, default="")
    u_no = models.CharField(max_length=40, default="")
    city = models.CharField(max_length=60)
    location = models.CharField(max_length=100, default="")
    ip_address = models.CharField(max_length=50, default="")
    

    def __str__(self):
        return self.username

class Forget(models.Model):
    id = models.BigAutoField
    email = models.CharField(max_length=50)
    u_no = models.CharField(max_length=50)
    is_delete = models.CharField(max_length=50, default=False)


    def __str__(self):
        return self.email


class MainData(models.Model):
    id = models.AutoField
    rf_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="Please specify Category")
    short_desc = models.CharField(max_length=200, default="Please specify desc")
    desc = models.CharField(max_length=5000)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="product/images", default="")
    status = models.CharField(max_length=50, default="Specify Status")
    pub_date = models.DateField()
    slug = models.CharField(max_length=200, default="/")
    page_name = models.CharField(max_length=200, default="")


    def __str__(self):
        return self.product_name

class NewsLetter(models.Model):
    email = models.CharField(max_length=80, default="")


    def __str__(self):
        return self.email


class CustomerReview(models.Model):
    no = models.IntegerField(default=0)
    image = models.ImageField(upload_to = "customerReview/images",default=" ")
    customer_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=5000)
    class1 = models.CharField(max_length=50, default=" ")


    def __str__(self):
        return self.customer_name

class HeadCarousel(models.Model):
    title=models.CharField(max_length=50)
    desc = models.CharField(max_length=5000)

    def __str__(self):
        return self.title