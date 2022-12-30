from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'materials'

urlpatterns = [
    path('categories/',CategoryCreateAndListView.as_view(),name='category'),
    path('categories/pop',CategoryAddPopup.as_view(),name='category_pop'),
    path('categories/<int:pk>',CategoryUpdateView.as_view(),name='category_update'),
    path('categories/<int:pk>/delete',CategoryDeleteView.as_view(),name='category_delete'),

    path('brands/',BrandCreateAndListView.as_view(),name='brand'),
    path('brands/pop',BrandAddPopup.as_view(),name='brand_pop'),
    path('brands/<int:pk>',BrandUpdateView.as_view(),name='brand_update'),
    path('brands/<int:pk>/delete',BrandDeleteView.as_view(),name='brand_delete'),

    path('units/',UnitCreateAndListView.as_view(),name='unit'),
    path('units/pop',UnitsAddPopup.as_view(),name='unit_pop'),
    path('units/<int:pk>',UnitUpdateView.as_view(),name='unit_update'),
    path('units/<int:pk>/delete',UnitDeleteView.as_view(),name='unit_delete'),

    path('add/',MaterialCreateView.as_view(),name='material_create'),
    path('material/pop/<str:target_id>',MaterialAddPopup.as_view(),name='material_pop'),
    path('material/pop/',MaterialAddPopup.as_view(),name='material_pop'),
    path('<int:pk>/update/',MaterialUpdateView.as_view(),name='material_update'),
    path('<int:pk>/delete/',MaterialDeleteView.as_view(),name='material_delete'),
    path('',MaterialListView.as_view(),name='material_list'),

    path('city/',CityCreateAndListView.as_view(),name='city'),
    path('city/pop',CityAddPopup.as_view(),name='city_pop'),
    path('city/<int:pk>',CityUpdateView.as_view(),name='city_update'),
    path('city/<int:pk>/delete',CityDeleteView.as_view(),name='city_delete'),
    
    path('warehouse/add/',WarehouseCreateView.as_view(),name='warehouse_create'),
    path('warehouse/pop',WarehouseAddPopup.as_view(),name='warehouse_pop'),
    path('warehouse/<int:pk>/update/',WarehouseUpdateView.as_view(),name='warehouse_update'),
    path('warehouse/<int:pk>/delete/',WarehouseDeleteView.as_view(),name='warehouse_delete'),
    path('warehouse/<int:pk>/transfer/',InventoryTransferView.as_view(),name='inventory_transfer'),
    path('warehouse/',WarehouseListView.as_view(),name='warehouse_list'),

    path('inventory/add/',InventoryCreateView.as_view(),name='inventory_create'),
    path('inventory/<int:pk>/update/',InventoryUpdateView.as_view(),name='inventory_update'),
    path('inventory/',InventoryListView.as_view(),name='inventory_list'),
    path('inventory_adj/',InventoryAdjListView.as_view(),name='inventory_adj_list'),

    path('purchases/',PurchasesListView.as_view(),name='purchase_list'),
    path('purchases/add/',PurchaseSimpleView.as_view(),name='purchase_create'),
    path('purchases/<int:pk>/',PurchaseDetailView.as_view(),name='purchase_detail'),

    path('transfer/',MaterialTransferCreateView.as_view(),name='transfer'),
    path('transfer_list/',TransferListView.as_view(),name='transfer_list'),
    path('transfer/<int:pk>/',TransferDetailView.as_view(),name='transfer_detail'),
    path('transfer/<int:pk>/delete',TransferDeleteView.as_view(),name='transfer_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
