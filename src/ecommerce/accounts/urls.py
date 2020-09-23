from django.urls import include, path, re_path
from .views import (
        AccountHomeView, 
        AccountEmailActivateView,
        # UserDetailUpdateView
        )

app_name = "accounts"

urlpatterns = [
    path("", AccountHomeView.as_view(), name='home'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name="email-activate"),
    path("email/resend-activation/", AccountEmailActivateView.as_view(), name="resend-activation")
#     url(r'^details/$', UserDetailUpdateView.as_view(), name='user-update'),
#     url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', 
        #     AccountEmailActivateView.as_view(), 
        #     name='email-activate'),
#     url(r'^email/resend-activation/$', 
        #     AccountEmailActivateView.as_view(), 
        #     name='resend-activation'),
]

# account/email/confirm/asdfads/ -> activation view