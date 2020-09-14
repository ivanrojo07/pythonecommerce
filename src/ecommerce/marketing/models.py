from django.db import models
from django.conf import settings
from .utils import Mailchimp
from django.db.models.signals import post_save, pre_save

# Create your models here.
class MarketingPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    mailchimp_subscribed = models.BooleanField(null=True, blank=True)
    mailchimp_msg = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # pass
        print("Add usert to mailchimp")
        status_code, data = Mailchimp().subcribed(instance.user.email)
        print(status_code, data)

post_save.connect(marketing_pref_create_receiver, sender=MarketingPreferences)

def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            status_code, data = Mailchimp().subcribed(instance.user.email)
        else:
            status_code, data = Mailchimp().unsubcribed(instance.user.email)
        
        if status_code == 200 and data['status'] == "subscribed":
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = data
        print(status_code, data)
    
pre_save.connect(marketing_pref_update_receiver,sender=MarketingPreferences)

def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):

    if created:
        MarketingPreferences.objects.get_or_create(user=instance)


post_save.connect(make_marketing_pref_receiver,sender=settings.AUTH_USER_MODEL)

