from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from products.models import Basket, Products, ProductsCategori, ProductImage, ProductSize
from django.shortcuts import render, redirect
from django.db.models import F
from urllib.parse import parse_qs
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
        context['selected_sizes'] = self.request.GET.get('size')
        context['selected_gender'] = self.request.GET.get('gender')
        context['selected_company'] = self.request.GET.get('company')
        context['companies'] = Products.objects.filter(company__isnull=False).\
            values_list('company', flat=True).distinct()

        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        categori_id = self.kwargs.get('categori_id')
        company = self.request.GET.get('company')
        gender = self.request.GET.get('gender')
        size = 'M' if self.request.GET.get('size') == 'MS' else self.request.GET.get('size')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        # Фильтрация по категории
        if categori_id:
            queryset = queryset.filter(category_id=categori_id)

        # Фильтрация по компании
        if company:
            queryset = queryset.filter(company__startswith=company)

        # Фильтрация по полу
        if gender:
            queryset = queryset.filter(gender=gender)

        # Фильтрация по размеру
        if size:
            # Фильтрация по размеру с использованием аннотации
            queryset = queryset.annotate(
                selected_size=F('sizes__size_name')
            ).filter(selected_size=size)


        # Фильтрация по цене
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


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


@login_required
def basket_update(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('basket_quantity_'):
                try:
                    basket_id = key.split('_')[-1]
                    quantity = int(value)

                    if quantity == 0:
                        basket_remove(request, basket_id)
                    else:
                        basket = Basket.objects.get(id=basket_id, user=request.user)
                        basket.quantity = quantity
                        basket.save()

                except (ValueError, Basket.DoesNotExist):
                    # Обработка исключений в случае, если value не является числом
                    # или если корзина с указанным ID не существует
                    basket_remove(request, basket_id)

    # Редирект на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'index'))





class ProductDeteilView(DetailView):
    model = Products
    template_name = 'products/deteil.html'
    context_object_name = 'deteil'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('product_detail', args=(self.object.slug,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Фильтрация изображений по ID товара
        context['images'] = ProductImage.objects.filter(product_id=self.object.id)

        # Фильтрация размеров по ID товара
        context['sizes'] = ProductSize.objects.filter(product_id=self.object.id)
        return context
