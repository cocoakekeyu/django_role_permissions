# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import PermissionView, RoleView, RoleDetailView

urlpatterns = [
    url(r'^permission/?$', PermissionView.as_view()),
    url(r'^role/?$', RoleView.as_view()),
    url(r'^role/(?P<pk>\d+)/?$', RoleDetailView.as_view()),
]
