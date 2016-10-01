from django.conf.urls import url
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout as logout_view

from . import views

urlpatterns = [
    url(r'register$', views.register, name='register'),
    url(r'thanks$', views.thanks, name='thanks'),
    url(r'accounts/login/$', login_view, name='login'),
    url(r'main$', views.main, name='main'),
    url(r'logout', logout_view, name='logout'),

    url(r'mark-school-paid', views.mark_school_paid, name='mark_school_paid'),
    url(r'mark-delegate-paid', views.mark_delegate_paid, name='mark_delegate_paid'),
    url(r'mark-transit-paid', views.mark_transit_paid, name='mark_transit_paid'),
]
