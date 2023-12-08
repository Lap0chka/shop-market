from django.contrib import admin

from orders.models import Orders

# Register your models here.


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'statuses')
    fields = ('id', 'created',
              ('first_name', 'last_name'),
              'email', 'basket_history', 'initiator',
              ('street', 'city', 'plz'),
              'statuses',
              )
    readonly_fields = ('id', 'created')
