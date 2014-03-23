from django.conf.urls import patterns, url
from bills import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about', views.about, name = 'about'),
        url(r'^addType/$', views.addType, name='addType'),	# added chapter 7 - fun with forms
        url(r'^type/(?P<type_name_url>\w+)/addBill/$', views.addBill, name='addBill'),  # added in chapter 7.exersises - fun with forms
        url(r'^type/(?P<type_name_url>\w+)/$', views.type, name='type'),  # added in chapter 6
        url(r'^register/$', views.register, name='register'),	# chapter 8 - user authentication
        url(r'^login/$', views.user_login, name='login'),	# chapter 8 - user authentication
        url(r'^restricted/', views.restricted, name='restricted'),	# chapter 8 - user authentication
        url(r'^logout/$', views.user_logout, name='logout'),    # chapter 8 - user authentication
        url(r'^search/$', views.search, name='search'),    # chapter 10 - external search API with BING
        )