from django.http import HttpResponse
from django.views.generic import TemplateView
from .mongo_storage_api import StorageManager
from .constants import *


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class HomeView(BaseView):
    template_name = 'home.html'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'LTGames'

        return context
