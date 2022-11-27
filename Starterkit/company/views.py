from django.shortcuts import render
from .forms import *
from django.views.generic.edit import FormView, CreateView
from .models import *
# Create your views here.


class newCompanyView(CreateView):
    model = Company
    fields = '__all__'
    # form_class =  CompanyForm
    template_name = 'form.html'
    success_url =  '/company/newCompany'
    


def newCompany(request):
    initial_data = {}
    final_form = { 'form_title': 'Validate',}
    if request.method == 'POST':
        a_form = AddressForm(request.POST)
        c_form = CompanyForm(request.POST)
        p_form = PersonForm(request.POST)
        if a_form.is_valid():
            x = a_form.save()
            initial_data['address'] = x.pk
        if c_form.is_valid():
            x = c_form.save()
            initial_data['company'] = x.pk
        if p_form.is_valid():
            p_form.save()
    a_form = AddressForm(initial=initial_data)
    for a in a_form:
        print('Label: ',a.label)
        print('element: ',a)
        print('id: ',a.id_for_label)
    a_form_title = 'Address'
    c_form = CompanyForm(initial=initial_data)
    c_form_title = 'Company Name'
    p_form = PersonForm(initial=initial_data)
    p_form_title = 'Contact Person'
    return render(request,'company/wizardForm.html',{
        'forms': [{
            'form': a_form,
            'form_title': a_form_title
        }, {
            'form': c_form,
            'form_title': c_form_title
        }, {
            'form': p_form,
            'form_title': p_form_title
        }, {

        } ]
    })
