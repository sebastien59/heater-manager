"""ThermoApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework import routers
from thermo import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
"""router.register(r'setups', views.GroupView)
router.register(r'rooms', views.RoomsView)
router.register(r'plugs', views.PlugsView)
router.register(r'sensors', views.SensorsView)
router.register(r'logs/sensors', views.LogsSensorsView)
router.register(r'logs/plugs', views.LogsPlugsView)"""

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^setups/?$', views.SetupView.as_view()),
    url(r'^setups/(?P<pk>[0-9]+)/?$', views.SetupDetailView.as_view()),
    url(r'^rooms/?$', views.RoomsView.as_view()),
    url(r'^rooms/(?P<pk>[0-9]+)/?$', views.RoomsDetailView.as_view()),
    url(r'^plugs/?$', views.PlugsView.as_view()),
    url(r'^plugs/(?P<pk>[0-9]+)/?$', views.PlugsDetailView.as_view({'get': 'list', 'put': 'update'})),
    #url(r'^plugs/(?P<pk>[0-9]+)/set_state/?$',views.PlugsDetailView.as_view()),
    url(r'^sensors/?$', views.SensorsView.as_view()),
    url(r'^sensors/(?P<pk>[0-9]+)/?$', views.SensorsDetailView.as_view()),
    url(r'^logs/sensors/?$', views.LogsSensorsView.as_view()),
    url(r'^logs/sensors/(?P<pk>[0-9]+)/?$', views.LogsSensorsDetailView.as_view()),
    url(r'^logs/plugs/?$', views.LogsPlugsView.as_view()),
    url(r'^logs/plugs/(?P<pk>[0-9]+)/?$', views.LogsPlugsDetailView.as_view()),
    url(r'^cron/CheckTemperature', views.CheckDataView.as_view())
]