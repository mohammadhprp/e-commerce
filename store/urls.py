from django.urls import path
from .views import store, cart, checkout, updateItem


urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),

    path('update_item/', updateItem, name='update-item'),

]
