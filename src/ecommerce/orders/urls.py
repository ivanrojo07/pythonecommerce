
from django.urls import path, re_path

from .views import (
                    OrderDetailView, 
                    OrderListView,
                    VerifyOwnership)

app_name = "orders"
urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('endpoint/verify/ownership/',VerifyOwnership.as_view(), name="verify-ownership"),
    re_path('detail/(?P<order_id>[0-9A-Za-z]+)/$',OrderDetailView.as_view(), name='detail'),

]
