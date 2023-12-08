from django.urls import path

from orders import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name='orders'),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name='order'),
    path("order-create", views.OrderCreateView.as_view(), name='order-create'),
    path("success", views.SuccessTemplateView.as_view(), name='success'),
    path("canceled", views.CanceledTemplateView.as_view(), name='canceled'),
]
