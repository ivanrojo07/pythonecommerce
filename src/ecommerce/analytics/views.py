import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from orders.models import Order
from django.db.models import Count, Sum, Avg
from django.utils import timezone

class SalesAjaxView(View):
    def get(self, request, *args,**kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5,number_of_weeks=5)
            if request.GET.get("type") == "week":
                days = 7
                start_date = timezone.now() - datetime.timedelta(days=days-1)
                datetime_list = []
                labels = []
                salesItem = []
                for x in range(0, days):
                    new_time = start_date + datetime.timedelta(days=x)

                    datetime_list.append(
                        new_time
                    )
                    labels.append(
                        new_time.strftime("%a")
                    )
                    new_qs = qs.filter(updated__day = new_time.day, updated__month=new_time.month)
                    sales_total = new_qs.totals_data()['total__sum']
                    if sales_total is None:
                        sales_total = 0
                    salesItem.append(
                        sales_total
                    )
                # print(datetime_list, labels)
                # data['labels']= ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
                data['labels']= labels

                # data['data']= [123, 131, 313, 12, 323, 3193, 655]
                data['data'] = salesItem
            if request.GET.get("type") == "4weeks":
                data['labels']= ["4 semanas", "3 semanas", "2 semanas", "1 semana", "Esta semana" ]
                current = 5
                data['data'] = []
                for i in range(0,5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()['total__sum']
                    if sales_total is None:
                        sales_total = 0
                    data['data'].append(sales_total)
                    current -= 1
                # print(data['data'])

                # data['data']= [433, 123, 313, 655]
        return JsonResponse(data)

class SalesView(LoginRequiredMixin,TemplateView):
    template_name="analytics/sales.html"

    def dispatch(self,*args,**kwargs):
        user = self.request.user
        if not user.is_staff:
            # return HttpResponse("Not Allowed", status=401)
            return render(self.request, "400.html",{})

        return super(SalesView, self).dispatch(*args,**kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args,**kwargs)
        # qs = Order.objects.all()
        qs = Order.objects.all().by_weeks_range(weeks_ago=10,number_of_weeks=10)
        context['today'] = qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
        context['this_week'] = qs.by_weeks_range(weeks_ago=1,number_of_weeks=1).get_sales_breakdown()
        context['last_four_week'] = qs.by_weeks_range(weeks_ago=5,number_of_weeks=4).get_sales_breakdown()

        # context['orders'] = qs
        # context['recent_orders'] = qs.recent().not_refunded()#[:5]
        # # recent_orders_total=0
        # # for i in context['recent_orders']:
        # #     recent_orders_total += i.total
        # # context['recent_orders_total'] = recent_orders_total
        # context['recent_orders_data']= context['recent_orders'].totals_data()
        # context["recent_orders_cart_data"] = context['recent_orders'].cart_data()
        # context['shipped_orders'] = qs.recent().not_refunded().by_status(status="shipped")#[:5]
        # context['shipped_orders_data'] = context['shipped_orders'].totals_data()
        # context['paid_orders'] = qs.recent().not_refunded().by_status(status="paid")#[:5]
        # context['paid_orders_data'] = context['paid_orders'].totals_data()
        return context
