from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name="sender",  null=True, blank=True, on_delete=models.CASCADE)
    recever = models.ForeignKey(User, related_name="recever", null=True, blank=True, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
 
class IndidualChat(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    
class GroupChat(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    admin = models.ForeignKey(User, related_name="admin", null=True, blank=True , on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="paticipants",)
    time_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + str(self.id)

    
class GroupMessage(models.Model):
    group = models.ForeignKey(GroupChat, null=True, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=240, null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    is_image = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.message + str(self.id) if self.message is not None else  str(self.id)

    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products")

class Orders(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)
