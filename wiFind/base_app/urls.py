from django.conf.urls import url
from . import views
from . import main

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='index'),  # TODO: user login/session/etc

    # url used when user selects create account in interface, creates new db entry and eth account
    url(r'^create_account/$', views.route_create_account, name='create_account'),

    # used for initial user login
    url(r'^login_attempt/$', views.route_login_attempt, name='login_attempt'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # user logout, btn click in nav bar
    url(r'^logout/$', views.logout, name='logout'),

    # when register node selected, find the available networks
    # url(r'^detect_wifi_networks/$', main.detect_wifi_networks, name='detect_wifi_networks'),

    # FindWifi View
    url(r'^find_wifi/$', views.FindWifi.as_view(), name='find_wifi'),

    # Register Wifi View
    url(r'^register_wifi/$', views.RegisterWifi.as_view(), name='register_wifi'),

    # When attempting to register a node
    url(r'^register_node/$', views.route_register_node, name='register_node')
]


