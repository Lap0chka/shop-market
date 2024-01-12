from django.urls import path

from products import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name='products'),
    path("<slug:slug>", views.ProductDeteilView.as_view(), name='product_detail'),
    path("categori/<int:categori_id>/", views.ProductListView.as_view(), name='categori'),
    path("page/<int:page>/", views.ProductListView.as_view(), name='paginator'),
    path("basket/add/<int:product_id>/", views.basket_add, name='basket_add'),
    path('basket/update/', views.basket_update, name='basket_update'),
    path("basket/del/<int:basket_id>/", views.basket_remove, name='basket_remove'),
    path("basket/del/<int:basket_id>/", views.basket_remove, name='basket_remove'),
]
