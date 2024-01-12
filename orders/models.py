from django.db import models

from products.models import Basket
from users.models import User

# Create your models here.


class Orders(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On way'),
        (DELIVERED, 'DELIVERED'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    plz = models.CharField(max_length=128)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    statuses = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id} {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.statuses = self.PAID
        self.basket_history = {
            'purchased_item': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
