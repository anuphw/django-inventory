from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from django.urls import reverse

class DealsListView(ListView):
    model = Deal
    template_name = 'deals/deals_list.html'

class DealsDetailView(DetailView):
    model = Deal
    template_name = 'deals/deal_detail.html'

class DealsCreateView(CreateView):
    model = Deal
    template_name = 'deals/deal_create.html'