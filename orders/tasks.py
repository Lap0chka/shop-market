from celery import shared_task
from django.core.mail import send_mail
from .models import Orders
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def order_created(order_id):
#Задание по отправке уведомления по электронной почте при успешном создании заказа.

    order = Orders.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,message, 'admin@myshop.com', [order.email])
    return mail_sent


@shared_task
def payment_completed(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа.
    """
    order = Orders.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop – Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,message, 'admin@myshop.com', [order.email])
    # сгенерировать PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0] / 'css/pdf.css')]#STATIC_ROOT
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # прикрепить PDF-файл
    email.attach(f'order_{order.id}.pdf', out.getvalue(),
    'application/pdf') # отправить электронное письмо
    email.send()