from django.contrib import admin
from .models import MarketingPreferences
# Register your models here.

class MarketingPreferencesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subscribed',"update"]
    readonly_fields = ["mailchimp_subscribed", "timestamp", "update"]
    class Meta:
        model = MarketingPreferences
        fields = ["user","subscribed","mailchimp_msg","mailchimp_subscribed", "timestamp", "update"]

admin.site.register(MarketingPreferences, MarketingPreferencesAdmin)