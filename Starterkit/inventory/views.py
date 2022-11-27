from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def allProducts(request):
    return render(request, 'inventory/products/allProducts.html')

def newProduct(request):
    return render(request, 'inventory/products/newProduct.html')

def allAdjustments(request):
    return render(request, 'inventory/adjustments/allAdjustments.html')

def newAdjustment(request):
    return render(request, 'inventory/adjustments/newAdjustment.html')

def allPurchases(request):
    return render(request, 'inventory/purchase/allPurchases.html')

def newPurchase(request):
    return render(request, 'inventory/purchases/newPurchase.html')

def allSales(request):
    return render(request, 'inventory/sales/allSales.html')

def newSale(request):
    return render(request, 'inventory/sales/newSale.html')

def allJobs(request):
    return render(request, 'inventory/jobs/allJobs.html')

def newJob(request):
    return render(request, 'inventory/jobs/newJob.html')