from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from orders.models import Orders

def order_pdf(obj):
    url = reverse('admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'statuses', order_pdf)
    fields = ('id', 'created',
              ('first_name', 'last_name'),
              'email', 'basket_history', 'initiator',
              ('street', 'city', 'plz'),
              'statuses',
              )
    readonly_fields = ('id', 'created')
