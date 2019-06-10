from django.conf.urls import patterns, url

from gears_ui import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setFreq$', views.setFreq, name='setFreq'),
    url(r'^setEnable$', views.setEnable, name='setEnable'),
    url(r'^getStatus$', views.getStatus, name='getStatus'),
)
