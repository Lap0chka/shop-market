from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from orders.form import OrdersForm
from orders.models import Orders
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEEBHOOK_SECRTET


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(CreateView):
    template_name = 'orders/orders-create.html'
    form_class = OrdersForm
    success_url = reverse_lazy('order-create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(self, request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderListView(ListView):
    template_name = 'orders/orders.html'
    queryset = Orders.objects.all()

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Orders


# @csrf_exempt
# def my_webhook_view(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#          payload, sig_header, endpoint_secret
#         )
#     except ValueError:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
#         session = stripe.checkout.Session.retrieve(
#           event['data']['object']['id'],
#           expand=['line_items'],
#         )
#         line_items = session
# # Fulfill the purchase...
#         fulfill_order(line_items)
#
#     # Passed signature verification
#     return HttpResponse(status=200)
#
#
# def fulfill_order(session):
#     order_id = int(session.metadata.order_id)
#     order = Orders.objects.get(id=order_id)
#     order.update_after_payment()

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload,sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
    # Недопустимая полезная нагрузка
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e: # Недопустимая подпись
        return HttpResponse(status=400)
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Orders.objects.get(id=session.client_reference_id)
            except Orders.DoesNotExist:
                return HttpResponse(status=404)
    # пометить заказ как оплаченный
            order.statuses = Orders.STATUSES.paid
            order.save()
    return HttpResponse(status=200)
