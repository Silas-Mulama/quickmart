from django.urls import path,include
from products.views import *
urlpatterns = [
    path('',products_lst,name='home'),
    path('products/',products_lst,name='products_list'),
    path('categories/',category_pg,name='category_list'),
    path('men-clothing/',menclothing,name='clothing_men'),
    path('men-clothing/',womenclothing,name='clothing_women'),
    path('sale-items/',saleitem,name='sale_items'),
    path('new-arrivals/',newarrivals,name='new_arrivals'),
    path('product_detail/',product_det,name='product_details'),

]
