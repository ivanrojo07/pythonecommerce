from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

# Create your models here.

class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) #User instance instace.id
    ip_address = models.CharField(max_length=220, blank= True, null= True) #IP Field
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE) # Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id
    content_object = GenericForeignKey('content_type','object_id') # Product instance
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s viewed %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Object viewed'