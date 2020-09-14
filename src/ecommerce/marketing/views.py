from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView
from django.shortcuts import render, redirect

# Create your views here.

from .forms import MarketingPreferencesForm
from .models import MarketingPreferences

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