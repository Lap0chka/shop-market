from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from products.models import Basket, Products, ProductsCategori

# Create your views here.


class IndexView(TemplateView):
    template_name = 'products/index.html'


class ProductListView(ListView):
    model = Products
    template_name = 'products/products.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductsCategori.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        categori_id = self.kwargs.get('categori_id')
        return queryset.filter(category_id=categori_id) if categori_id else queryset


@login_required
def basket_add(requset, product_id):
    product = Products.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=requset.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=requset.user, product=product, quantity=1)
    else:
        basket = baskets.last()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(requset.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def products(request,categori_id=None,page_number=1):
#     products= Products.objects.filter(category_id=categori_id) if categori_id else Products.objects.all()
#     per_page = 6
#     paginator = Paginator(products,per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'products': products_paginator,
#         'categories':ProductsCategori.objects.all()
#     }
#     return render(request,'products/products.html',context)
