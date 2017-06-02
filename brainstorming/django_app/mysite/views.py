from django.http import HttpResponse
from django.views.generic import TemplateView
from .mongo_storage_api import StorageManager
from .constants import *

storage_manager = StorageManager('localhost', 27017, 'lt_game')

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


class DashboardView(BaseView):
    template_name = 'dashboard.html'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_account_info(kwargs['username'])
        return context

    def get_account_info(self, username):
        info = {}
        cursor = storage_manager.find(USERS_COLLECTION, {USERNAME: username})
        if cursor.count():
            info['username'] = cursor[0][USERNAME]
            info['email'] = cursor[0][EMAIL]
            info['balance'] = cursor[0][BALANCE]
        return info


class HighLowView(BaseView):
    template_name = 'highLow.html'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class InvestView(BaseView):
    template_name = 'invest.html'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
