from django.views.generic import TemplateView
from django.http import JsonResponse
from base_app.constants import *
from base_app.storage.mongo_storage_api import StorageManager
from base_app.eth_api import *
from base_app.main import *


# initialize the storage system
storage_manager = StorageManager(MONGO_IP, MONGO_PORT, WIFIND_DB)


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

        return context


class DashboardView(BaseView):
    template_name = 'dashboard.html'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(BaseView):
    template_name = 'login.html'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FindWifi(BaseView):
    template_name = 'findWiFi.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        networks = detect_wifi_networks()
        context['networks'] = networks

        return context


class RegisterWifi(BaseView):
    template_name = 'registerWiFi.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        networks = detect_wifi_networks()
        context['networks'] = networks

        return context


# user logout from landing page
def logout(request):
    # delete this user id from the session object
    del request.session[USER_ID]

    return JsonResponse({})


# *****************
# **** ROUTING ****
# *****************
# Routing, pass instances of storageManager
# create new user account, routed to eth_api.create_account
def route_create_account(request):
    return JsonResponse(create_account(request, storage_manager))


# user login from landing page, routed to main.login
def route_login_attempt(request):
    return JsonResponse(login(request, storage_manager))


# when register wifi selected, routed to main.register_node
def route_register_node(request):
    return JsonResponse(register_node(request, storage_manager))
