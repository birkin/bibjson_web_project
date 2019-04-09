# -*- coding: utf-8 -*-

from bib_ourl_api_app import views
from django.conf.urls import url
from django.views.generic import RedirectView
# from django.contrib import admin


# admin.autodiscover()


urlpatterns = [

    # url( r'^admin/', admin.site.urls ),

    url( r'^v1/ourl_to_bib/$', views.ourl_to_bib, name='ourl_to_bib_url' ),

    url( r'^v1/bib_to_ourl/$', views.bib_to_ourl, name='bib_to_ourl' ),

    # url( r'^access_test/$', views.access_test, name='access_test_url' ),

    url( r'^info/$', views.info, name='info_url' ),
    url( r'^error_check/$', views.error_check, name='error_check' ),  # only generates error if DEBUG == True

    url( r'^$',  RedirectView.as_view(pattern_name='info_url') ),

    ]
