from django.conf.urls import patterns, url

from app.home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'abc/$', views.faq, name='index'),
    # url(r'about/$', views.about, name='index'),
    # url(r'terms_and_conditions/$', views.terms_and_conditions, name='index'),
)