from django.urls import path, include

from shop import views

urlpatterns =[
    path('product/', views.ProductView.as_view(), name='products'),
]