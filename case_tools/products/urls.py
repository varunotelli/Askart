from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
from . import views
from django.contrib.auth.views import logout
from django.conf import settings
app_name='products'
urlpatterns = [
    url(r'^index/$', views.display,name='index'),
    url(r'^error/$', views.error, name='error'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
url(r'^$', login, {'template_name':'products/login.htm'}),
url(r'^autocomplete/$',views.AutoCompleteView.as_view(), name='autocomplete'),
    url(r'^item/(?P<name>.*)/$',views.details,name='details'),
url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    
]
