from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Products, ProductsCategori


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        responce = self.client.get(path)
        self.assertEquals(responce.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(responce, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.products = Products.objects.all()

    def test_list(self):
        path = reverse('products')
        responce = self.client.get(path)
        self._common_tests(responce)
        self.assertEquals(list(responce.context_data['object_list']), list(self.products)[:6])

    def test_list_category(self):
        category = ProductsCategori.objects.first()
        path = reverse('categori', kwargs={'categori_id': category.id})
        responce = self.client.get(path)

        self._common_tests(responce)
        self.assertEquals(
            list(responce.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
            )

    def _common_tests(self, responce):
        self.assertEquals(responce.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(responce, 'products/products.html')
