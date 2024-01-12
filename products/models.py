import stripe
from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from users.models import User
from django.utils import timezone

# Create your models here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductsCategori(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=256)
    gender_choices = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('U', 'Унисекс'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, default='U')
    slug = models.SlugField(max_length=250, default=None)
    company = models.CharField(max_length=128, default=None)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quanity = models.PositiveIntegerField(default=0)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(ProductsCategori, on_delete=models.CASCADE)



    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Product: {self.name}| Categories: {self.category.name}'

    def upload_to(self, filename):
        # Генерация пути для загрузки изображения
        return f'products_image/{self.name}/{filename}'

    # Поле для основного изображения продукта
    main_image = models.ImageField(upload_to=upload_to, default=None)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.stripe_product_price_id:
            stripe_products_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_products_price['id']
        super(Products, self).save()

    def create_stripe_product_price(self):
        stripe_products = stripe.Product.create(name=self.name)
        stripe_products_price = stripe.Price.create(
            product=stripe_products['id'],
            unit_amount=round(self.price*100),
            currency='eur',
        )
        return stripe_products_price


class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='additional_product_images')

    def upload_to(self, filename):
        # Генерация пути для загрузки изображения
        return f'products_image/{self.product.name}/{filename}'

    image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return f'Additional Image for {self.product.name}'


class ProductSize(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='sizes')
    size_name = models.CharField(max_length=50)
    bust_size = models.PositiveIntegerField(null=True, blank=True)
    waist_size = models.PositiveIntegerField(null=True, blank=True)
    hip_size = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.size_name


class BasketQuearySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuearySet.as_manager()

    def __str__(self):
        return f'User: {self.user.username}| Goods: {self.product}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'products_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
