"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from . import login
from . import highlow

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^dashboard/(?P<username>[\w\-]+)', views.DashboardView.as_view(), name='dashboard'),
    url(r'^highlow/', views.HighLowView.as_view(), name='highlow'),
    url(r'^invest/', views.InvestView.as_view(), name='invest'),
    url(r'^change_password/', login.change_password, name='change_password'),
    url(r'^attempt_login/', login.attempt_login, name='attempt_login'),
    url(r'^create_user/', login.create_user, name='create_user'),
    url(r'^update_user/', login.update_user, name='update_user'),
    url(r'^get_account_address/', login.get_account_address, name='get_account_address'),
    url(r'^update_balance/', login.update_balance, name='update_balance'),
    url(r'^read_highlow_contract/$', highlow.read_highlow_contract, name='read_highlow_contract'),
]
