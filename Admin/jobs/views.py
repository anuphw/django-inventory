from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class JobsListView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Jobs List"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/joblist.html',greeting)

class JobsGridView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Jobs Grid"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/jobgrid.html',greeting)  

class JobsApplyView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Jobs Apply"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/jobapply.html',greeting)              

class JobsDetailsView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Jobs details"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/jobdetails.html',greeting)                

class JobsCategoriesView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Jobs Categories"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/jobcategories.html',greeting)   

class CandidateListView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Candidate List"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/candidatelist.html',greeting)  

class CandidateOverviewView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Candidate Overview"
        greeting['pageview'] = "Jobs"
        return render (request,'jobs/candidateoverview.html',greeting)                            