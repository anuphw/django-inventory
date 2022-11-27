from django.urls import path,include
from .views import *


urlpatterns = [
    path('allProducts',allProducts,name="allProducts"),
    path('newProduct',newProduct,name="newProduct"),
    path('allPurchases',allPurchases,name="allPurchases"),
    path('newPurchase',newPurchase,name="newPurchase"),
    path('allAdjustments',allAdjustments,name="allAdjustments"),
    path('newAdjustment',newAdjustment,name="newAdjustment"),
    path('allSales',allSales,name="allSales"),
    path('newSale',newSale,name="newSale")
]