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
from . import testCam

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^discover_usb_devices', testCam.discover_usb_devices, name='discover_usb_devices'),
    url(r'^register_new_device', testCam.register_new_device, name='register_new_device'),
    url(r'^push_data', testCam.push_data_packet, name='push_data'),
]
