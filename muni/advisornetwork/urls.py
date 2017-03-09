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

    # /advisor/{id}/delete
    url(r'advisor/(?P<advisor>[0-9]+)/delete', views.advisor_delete, name='advisor_delete'),

    # /advisor/{id}/edit
    url(r'advisor/(?P<advisor>[0-9]+)/edit', views.advisor_edit, name='advisor_edit'),

    # /delegate/{id}/delete
    url(r'delegate/(?P<delegate>[0-9]+)/delete', views.delegate_delete, name='delegate_delete'),

    # /delegate/{id}/edit
    url(r'delegate/(?P<delegate>[0-9]+)/edit', views.delegate_edit, name='delegate_delete'),

    # /addadvisor
    url(r'addadvisor', views.add_advisor, name='add_advisor'),

    # /adddelegate
    url(r'adddelegate', views.add_delegate, name='add_delegate'),

    # /positionpapers
    url(r'positionpapers', views.position_papers, name='position_papers'),

    # /print
    url(r'print', views.print_q_submit, name='print_q_submit')
]
