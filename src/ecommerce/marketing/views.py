from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect


# Create your views here.

from .mixins import CsrfExemptMixin
from .utils import Mailchimp
from .forms import MarketingPreferencesForm
from .models import MarketingPreferences

MAILCHIMP_EMAIL_LIST_ID = getattr(settings,"MAILCHIMP_EMAIL_LIST_ID",None)

class MarketingPreferencesUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferencesForm
    template_name = "base/forms.html"
    success_url = "/settings/email/"
    success_message = "Your email preferences have been updated. Thank you."
    
    def dispatch(self,*args,**kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login/?next=/settings/email/')#HttpResponse("Not allowed",status=400)
        return super(MarketingPreferencesUpdateView,self).dispatch(*args,**kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferencesUpdateView, self).get_context_data(*args,**kwargs)
        context['title'] = "Update Email Preferences"
        return context
    
    def get_object(self):
        user = self.request.user
        # if not user.is_authenticated:
        #     return HttpResponse("Not allowed",status=400)
        obj, created = MarketingPreferences.objects.get_or_create(user=user)
        return obj


class MailchimpWebhookView(CsrfExemptMixin,View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get('type')
            email =  data.get('data[email]')
            response_status, response = Mailchimp().check_subcription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False,False)

            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreferences.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed,mailchimp_msg=str(data)) 
        return HttpResponse("Thank you",status=200)
    