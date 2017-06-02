from django.shortcuts import render
from django.views.generic import TemplateView, ListView


# Create your views here.
class LandingPage(TemplateView):
    template_name = 'landing_page.html'

    # def get_context_data(self, **kwargs):
    #     context = super().__init__()